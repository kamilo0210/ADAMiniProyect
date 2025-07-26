import os
import time
from merge_abb.abb import ABB
from merge_abb.merge_sort import merge_sort
from heap_sort.heap_sort import heap_sort
import estadisticas

class Encuestado:
    def __init__(self, id_, nombre, experticia, opinion):
        self.id = id_
        self.nombre = nombre
        self.experticia = experticia
        self.opinion = opinion

class Pregunta:
    def __init__(self, id_preg, encuestados_ids):
        self.id = id_preg
        self.enc_ids = encuestados_ids
        self.enc = []

    def compute_stats(self):
        ops = [e.opinion for e in self.enc]
        exs = [e.experticia for e in self.enc]
        self.avg_op = estadisticas.promedio(ops)
        self.avg_ex = estadisticas.promedio(exs)
        # mediana necesita lista ordenada por opinión
        # la fija en main con preg.med
        self.med     = None
        self.mod     = estadisticas.moda(ops)
        self.ext     = estadisticas.extremismo(ops)
        self.cons    = estadisticas.consenso(ops)

class Tema:
    def __init__(self, id_tema, preguntas):
        self.id = id_tema
        self.preguntas = preguntas
    def compute_stats(self):
        ops = [p.avg_op for p in self.preguntas]
        exs = [p.avg_ex for p in self.preguntas]
        self.avg_avg_op = estadisticas.promedio(ops)
        self.avg_avg_ex = estadisticas.promedio(exs)
        self.total_enc  = sum(len(p.enc) for p in self.preguntas)

def parse_file(path):
    with open(path, encoding='utf-8') as f:
        lines = [l.strip() for l in f.readlines()]

    # separador
    sep = next(i for i,v in enumerate(lines) if v=="")
    enc_lines = [l for l in lines[:sep] if l]
    rest      = lines[sep+1:]

    # armar temas
    temas_braces, current = [], []
    for l in rest:
        if not l:
            if current:
                temas_braces.append(current)
                current=[]
        else:
            current.append(l)
    if current: temas_braces.append(current)

    # parsear encuestados
    enc_dict = {}
    for idx, line in enumerate(enc_lines, start=1):
        nombre, e_part, o_part = [p.strip() for p in line.split(",")]
        exp = int(e_part.split(":")[1])
        op  = int(o_part.split(":")[1])
        enc_dict[idx] = Encuestado(idx, nombre, exp, op)

    # parsear preguntas y temas
    temas = []
    for ti, braces in enumerate(temas_braces, start=1):
        preguntas=[]
        for pj, brace in enumerate(braces, start=1):
            body = brace.strip("{} ")
            ids = [int(x) for x in body.split(",")] if body else []
            pid = f"{ti}.{pj}"
            preguntas.append(Pregunta(pid, ids))
        temas.append(Tema(ti, preguntas))

    return temas, enc_dict

def sort_encuestados(enc_list, estrategia):
    if estrategia == 1:
        bst = ABB()
        for e in enc_list:
            bst.insert((e.opinion, e.experticia), e)
        return bst.traverse_desc()
    else:
        return heap_sort(enc_list, lambda e: (e.opinion, e.experticia))

def main():
    ruta = input("Ruta del archivo de encuesta (./encuestas/archivo.txt): ")
    estr = int(input("Seleccione estrategia (1-Merge+BST, 2-Heap): "))
    t0   = time.time()

    temas, enc_dict = parse_file(ruta)

    # 1) Estadísticas por pregunta y mediana
    for t in temas:
        for p in t.preguntas:
            p.enc = [enc_dict[i] for i in p.enc_ids]
            p.compute_stats()
            # para la mediana de opinión:
            sorted_enc = sort_encuestados(p.enc, estr)
            p.med = estadisticas.mediana([e.opinion for e in sorted_enc])
        t.compute_stats()

    # 2) Ordenar preguntas dentro de cada tema
    key_p = lambda p: (p.avg_op, p.avg_ex, len(p.enc))
    for t in temas:
        if estr==1:
            t.preguntas = merge_sort(t.preguntas, key_p)
        else:
            t.preguntas = heap_sort(t.preguntas, key_p)

    # 3) Ordenar temas
    if estr==1:
        temas = merge_sort(temas, lambda t: (t.avg_avg_op, t.avg_avg_ex, t.total_enc))
    else:
        temas = heap_sort(temas, lambda t: (t.avg_avg_op, t.avg_avg_ex, t.total_enc))

    dt = time.time()-t0

    # 4) Impresión de resultados por tema y pregunta
    print(f"\nTiempo de ordenamiento: {dt:.6f}s\n")
    print("Resultados de la encuesta:\n")
    for t in temas:
        print(f"[{t.avg_avg_op:.2f}] Tema {t.id}:")
        for p in t.preguntas:
            ids = ", ".join(str(e.id) for e in sort_encuestados(p.enc, estr))
            print(f"  [{p.avg_op:.2f}] Pregunta {p.id}: ({ids})")
        print()

    # 5) Lista de encuestados con detalle (orden: exp desc, id desc)
    all_enc = list(enc_dict.values())
    if estr == 1:
        enc_list = merge_sort(all_enc, lambda e: (e.experticia, e.id))
    else:
        enc_list = heap_sort(all_enc, lambda e: (e.experticia, e.id))

    print("Lista de encuestados:")
    for e in enc_list:
        print(f" ({e.id}, Nombre:'{e.nombre}', Experticia:{e.experticia}, Opinión:{e.opinion})")
    print()

    # 6) Estadísticas globales
    qs = [p for t in temas for p in t.preguntas]
    best = lambda fn: max(qs, key=fn)
    worst= lambda fn: min(qs, key=fn)

    print("Resultados:")
    print(f"  Pregunta con mayor promedio de opinion: [{best(lambda p:p.avg_op).avg_op:.2f}] Pregunta: {best(lambda p:p.avg_op).id}")
    print(f"  Pregunta con menor promedio de opinion: [{worst(lambda p:p.avg_op).avg_op:.2f}] Pregunta: {worst(lambda p:p.avg_op).id}")
    print(f"  Pregunta con mayor promedio de experticia: [{best(lambda p:p.avg_ex).avg_ex:.2f}] Pregunta: {best(lambda p:p.avg_ex).id}")
    print(f"  Pregunta con menor promedio de experticia: [{worst(lambda p:p.avg_ex).avg_ex:.2f}] Pregunta: {worst(lambda p:p.avg_ex).id}")
    print(f"  Pregunta con Mayor mediana de opinion: [{best(lambda p:p.med).med:.2f}] Pregunta: {best(lambda p:p.med).id}")
    print(f"  Pregunta con menor mediana de opinion: [{worst(lambda p:p.med).med:.2f}] Pregunta: {worst(lambda p:p.med).id}")
    print(f"  Pregunta con mayor moda de opinion: [{best(lambda p:p.mod).mod:.2f}] Pregunta: {best(lambda p:p.mod).id}")
    print(f"  Pregunta con menor moda de opinion: [{worst(lambda p:p.mod).mod:.2f}] Pregunta: {worst(lambda p:p.mod).id}")
    print(f"  Pregunta con mayor extremismo: [{best(lambda p:p.ext).ext:.2f}] Pregunta: {best(lambda p:p.ext).id}")
    print(f"  Pregunta con mayor consenso: [{best(lambda p:p.cons).cons:.2f}] Pregunta: {best(lambda p:p.cons).id}")

if __name__ == "__main__":
    main()

