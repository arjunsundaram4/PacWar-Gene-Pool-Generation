import random

def read_genes(file):
    f = open(file, "r")
    lst = []
    for l in f:
        lst.append(string_to_gene(l))
    return lst

def write_gene(gene, score, file):
    f = open(file, "w")
    f.write(gene, score)

def write_genes(genes, file):
    f = open(file, "w")
    for t in genes:
        f.write(str(t[0])+" "
            +str(t[1])+"\n")


def write_winners(genes,file):
    f=open(file, "a")
    f.write(str(genes[0])+" "
            +str(genes[1]))
    f.write("\n")

def initialize_winners(size):
    f = open("winners.txt", "w")
    for i in range(size):
        gene = random_gene()
        f.write(str(gene)+" " +str(0.00)+"\n")

def clear_winners():
    f = open("winners.txt", "w")
    f.truncate(0)

def read_winners():
    return read_genes("winners.txt")


def string_to_gene(s):
    s=s.rsplit(" ",1)
    gene =eval(s[0])
    score = float(s[1])
    return (gene, score)

def random_gene():
    gene = []
    for i in range(50):
        gene.append(random.choice([0,1,2,3]))
    return gene