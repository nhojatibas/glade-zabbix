#!/usr/bin/python
# -*- coding: utf-8 -*-

# Carregando bibliotecas

# Glade (carregando bibliotecas do Glade)
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Zabbix (carregando biblioteca da API do Zabbix e biblioteca de funcoes criadas)
from zabbix_api import ZabbixAPI
from zabbix_functions import *

# Bibliotecas de apoio
from datetime import datetime, date, time
import time as t


# Constantes
vServer = "http://monitor.ciasc.gov.br"
vUserName = "nholiveira@ciasc.sc.gov.br"
vPassword = "211172"

####################################
# Abrindo a sessão com o servidor zabbix
vZapi=ZabbixAPI(server=vServer, log_level=0)
vZapi.login(vUserName, vPassword)

# Buscando a lista de grupos no servidor Zabbix
vGroupListIni=vZapi.hostgroup.get({"output": ["name", "groupid"]})

class _cruza_grupo:
    def __init__(self):

        # Carrega do Glade os elementos da janela principal (cruza_grupo.glade), em variaveis self.glade
        self.glade=Gtk.Builder()
        self.glade.add_from_file("cruza_grupo.glade")
	self.glade.connect_signals(self) 

        self.glade.janela_principal=self.glade.get_object("_janela_principal")

        self.glade.treeview_lista_origem=self.glade.get_object("_treeview_lista_origem")
        self.glade.liststore_lista_origem=self.glade.get_object("_liststore_lista_origem")

        self.glade.button_refresh=self.glade.get_object("_button_refresh")
        self.glade.entry_filtragrupo=self.glade.get_object("_entry_filtragrupo")

        self.glade.button_add=self.glade.get_object("_button_add")
        self.glade.button_remove=self.glade.get_object("_button_remove")

        self.glade.button_search=self.glade.get_object("_button_search")

        self.glade.treeview_lista_destino=self.glade.get_object("_treeview_lista_destino")
	self.glade.liststore_lista_destino=self.glade.get_object("_liststore_lista_destino")

        # Carrega do Glade os elementos da sub janela (cruza_grupo_sub.glade), em variaveis self.glade.sub
#        self.glade.sub=Gtk.Builder()
#        self.glade.sub.add_from_file("cruza_grupo_sub.glade")
#        self.glade.sub.connect_signals(self)

#        self.glade.sub.janela_principal=self.glade.sub.get_object("_janela_principal_sub")


# Declarando o filtro a ser aplicado na "self.glade.liststore_lista_origem"
        self.treemodelfilter_lista_origem=self.glade.liststore_lista_origem.filter_new()
        self.treemodelfilter_lista_origem.set_visible_func(self.treemodelfilter_lista_origem_func)

# Cargas iniciais
        for grupo in vGroupListIni:
            self.glade.liststore_lista_origem.append([grupo['name']])

# Colocando o loop do Gtk para rodar
        self.glade.janela_principal.show_all()

    def run(self):
        Gtk.main()


# Função de filtro a ser aplicado em "self.glade.treeview_lista_origem"
    def treemodelfilter_lista_origem_func(self, model, iter, data):
        if len(self.current_filter_lista_origem) < 1:
            return True
        else:
            return self.current_filter_lista_origem in model[iter][0]

        
# Ligando os SINAIS do Glade a funções da classe (no Glade chamadas de Handler)

# Sinais da Janela Principal

# Fechando a aplicacao
    def onDeleteWindow(self, *args):
 	Gtk.main_quit(*args)

# Pressionando o botão "atualiza"
    def onButtonRefreshClicked(self, *args):
        self.glade.treeview_lista_origem.set_model(self.treemodelfilter_lista_origem)    # define o moldel do filtro como model a ser exibido pela treeview
        self.current_filter_lista_origem=self.glade.entry_filtragrupo.get_text()         # pega o parâmetro de filtragem do campo - self.glade.entry_filtragrupo.get_text() 
        self.treemodelfilter_lista_origem.refilter()                                     # aplica o filtro

# Pressionando o botão "+" (add)
    def onButtonAdd_clicked(self, *args):
        _treeview_origem_full = self.glade.treeview_lista_origem.get_selection()
        _treeview_origem_selected = _treeview_origem_full.get_selected()
        if _treeview_origem_selected[1] != None:
            (_modelo, _iter) = _treeview_origem_selected
            print "selected-->", _modelo[_iter], " : ",  _modelo[_iter][0], " : ", _iter.stamp, " : ", type(_iter)
            print self.glade.button_search.get_events()
            if _modelo[_iter][0] not in [_linha[0] for _linha in self.glade.liststore_lista_destino]: # Verifica se existe na lista para adicionar (só se nao existe)
                self.glade.liststore_lista_destino.append([_modelo[_iter][0]])

# Pressionando o botão "-" (remove)
    def onButtonRemove_clicked(self, *args):
        _treeview_destino_full = self.glade.treeview_lista_destino.get_selection()
        _treeview_destino_selected = _treeview_destino_full.get_selected()
        if _treeview_destino_selected[1] != None:
            (_modelo, _iter) = _treeview_destino_selected
            self.glade.liststore_lista_destino.remove(_iter)

# Pressionando o botao "Procurar"
#    def onButtonSearch_clicked(self, *args):
    def on(self, *args):
        print "Procurou"
#        self.glade.sub.janela_principal.show_all()


# Sinais da Sub Janela
#    def onsubDeleteWindow(self, *args):
#        Gtk.main_quits(*args)



_my_app=_cruza_grupo()
_my_app.run()
