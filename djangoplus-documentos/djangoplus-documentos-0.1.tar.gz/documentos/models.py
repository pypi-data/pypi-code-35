# -*- coding: utf-8 -*-

from djangoplus.db import models
from enderecos.models import Municipio, Estado


class Certidao(models.Model):
    tipo = models.CharField(verbose_name='Tipo', choices=[[x, x] for x in ['Nascimento', 'Casamento']])
    numero = models.CharField(verbose_name='Número')
    cartorio = models.CharField(verbose_name='Cartório')
    livro = models.CharField(verbose_name='Livro')
    folha = models.CharField(verbose_name='Folha')
    data = models.DateField(verbose_name='Data')
    municipio = models.ForeignKey(Municipio, verbose_name='Município', lazy=True)

    fieldsets = (
        ('Dados Gerais', {'fields': ('tipo', ('numero', 'cartorio'), ('livro', 'folha'), ('data', 'municipio'))}),
    )

    class Meta:
        verbose_name = 'Certidão'
        verbose_name_plural = 'Certidões'

    def __str__(self):
        return self.numero


class RG(models.Model):
    numero = models.CharField(verbose_name='Número')
    data = models.DateField(verbose_name='Data de Expedição')
    orgao = models.CharField(verbose_name='Orgão Expedidor')
    uf = models.ForeignKey(Estado, verbose_name='UF')

    fieldsets = (
        ('Dados Gerais', {'fields': (('numero', 'data'), ('orgao', 'uf'))}),
    )

    class Meta:
        verbose_name = 'RG'
        verbose_name_plural = 'RGs'

    def __str__(self):
        return self.numero


class CertificadoMilitar(models.Model):
    numero = models.CharField(verbose_name='Número')
    serie = models.CharField(verbose_name='Série')
    categoria = models.CharField(verbose_name='Categoria', null=True, blank=True)

    fieldsets = (
        ('Dados Gerais', {'fields': (('numero', 'serie', 'categoria'),)}),
    )

    class Meta:
        verbose_name = 'Certificado Militar'
        verbose_name_plural = 'Certificado Militars'

    def __str__(self):
        return self.numero


class TituloEleitor(models.Model):

    numero = models.IntegerField(verbose_name='Número')
    zona = models.CharField(verbose_name='Zona')
    secao = models.CharField(verbose_name='Seção')
    municipio = models.ForeignKey(Municipio, verbose_name='Município', lazy=True)

    fieldsets = (
        ('Dados Gerais', {'fields': (('numero', 'zona'), ('secao', 'municipio'))}),
    )

    class Meta:
        verbose_name = 'Título de Eleitor'
        verbose_name_plural = 'Títulos de Eleitores'

    def __str__(self):
        return self.numero
