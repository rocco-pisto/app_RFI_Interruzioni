from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from datetime import datetime
import calendar
import string

import os

from DrawPanel import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Interruzioni RFI")


        # cartelle e file
        self.workFold = os.path.expanduser("~")
        self.workFold = os.path.join(self.workFold, "Documents")
        self.workFold = os.path.join(self.workFold, "Grafico Interruzioni")


        # definizione layout base [comandi, grafico]
        lay_base = QHBoxLayout()
        dim_lay_base = [8, 12]

        # definizione layout comandi seperazione V
        lay_comV = QVBoxLayout()
        lay_base.addLayout(lay_comV, dim_lay_base[0])

        
        # pannello plot
        self.Panel = DrawPanel()
        lay_base.addWidget(self.Panel, dim_lay_base[1])



        ## griglia comandi
        # dimensioni orizontali
        dim_lay_comH = []
        dim_lay_comH.append([1, 1, 1, 1, 1]) # 0: riga calendario
        dim_lay_comH.append([]) # 1: spazio
        dim_lay_comH.append([1, 1, 1, 1, 1]) # 2: riga load stazioni e carica riprogrammate e settimana
        dim_lay_comH.append([]) # 3: spazio
        dim_lay_comH.append([1, 1, 1, 1, 1]) # 4: riga n ord
        dim_lay_comH.append([]) # 5: spazio
        dim_st = [4, 2 , 1, 1, 1]
        dim_lay_comH.append(dim_st) #6: A_ST
        dim_lay_comH.append(dim_st) #7: DA
        dim_lay_comH.append(dim_st) #8: A
        dim_lay_comH.append([]) #9: spazio
        dim_lay_comH.append([2, 4, 1, 2]) #10: binario e alimentazione
        dim_lay_comH.append([]) #11: spazio
        dim_lay_comH.append([2, 1]) # 12: riga input time e tabella
        dim_lay_comH.append([]) #13: spazio
        dim_lay_comH.append([1, 1, 1, 2]) # 14: riga plot e salva 


        N_lay_comV_el = len(dim_lay_comH)

        # dimensioni verticali
        dim_lay_comV = []
        for i in range(N_lay_comV_el):
            dim_lay_comV.append(1)
            if i == 12:
                dim_lay_comV[i] = 3

        # dimensioni box timing
        dim_lay_days = [2, 1]
        dim_lay_hour = [1, 1, 1]

        
        lay_comH = []
        for i in range(N_lay_comV_el):
            if dim_lay_comH[i]:
                lay_comH.append(QHBoxLayout())
                lay_comV.addLayout(lay_comH[i], dim_lay_comV[i])
            else:
                lay_comH.append("")
                lay_comV.addStretch( dim_lay_comV[i])

        

        self.fontSize = 12

        r = 0
        self.Mese = QSpinBox()
        lay_comH[r].addWidget(self.Mese, dim_lay_comH[r][0] )
        lay_comH[r].addWidget(QLabel("Mese"), dim_lay_comH[r][1] )

        self.Anno = QSpinBox()
        lay_comH[r].addWidget(self.Anno, dim_lay_comH[r][2] )
        lay_comH[r].addWidget(QLabel("Anno"), dim_lay_comH[r][3] )
        
        self.PrintCal = QPushButton("Calendario")
        self.PrintCal.clicked.connect(self.setCalendar)
        lay_comH[r].addWidget(self.PrintCal, dim_lay_comH[r][4] )


        r = r +2
        self.LoadStat = QPushButton("Stazioni")
        self.LoadStat.clicked.connect(self.changeStations)
        lay_comH[r].addWidget(self.LoadStat, dim_lay_comH[r][0] )


        self.Riprogram = QPushButton("Riprogramma")
        self.Riprogram.clicked.connect(self.loadFile)
        lay_comH[r].addWidget(self.Riprogram, dim_lay_comH[r][1] )

        lay_comH[r].addStretch(dim_lay_comH[r][2])
        self.SelWeek = QComboBox()
        lay_comH[r].addWidget(self.SelWeek, dim_lay_comH[r][3])
        lay_comH[r].addWidget(QLabel("Settimana"), dim_lay_comH[r][4])


        r = r +2
        self.nOrd = QSpinBox()
        self.nOrd.setValue(1)
        self.nOrd.valueChanged.connect(self.showOrdData)
        lay_comH[r].addWidget(self.nOrd, dim_lay_comH[r][0] )
        lay_comH[r].addWidget(QLabel("N° ORD"), dim_lay_comH[r][1] )

        r = r+2
        labels = ["A. ST.", "DA", "A"]
        check_lab = ["(S)", "(I)", "(I)"]
        keys = ["AMB", "DA", "A"]
        self.SelStat = {}
        self.CheckStat = {}
        for i in range(3):
            self.SelStat[keys[i]] = QComboBox() # salvo le selezioni delle stazioni in un dizionario
            lay_comH[r+i].addWidget(self.SelStat[keys[i]], dim_lay_comH[r+i][0])
            lay_comH[r+i].addWidget(QLabel(labels[i]), dim_lay_comH[r+i][1])

            self.CheckStat[keys[i]] = QCheckBox()
            lay_comH[r+i].addWidget(self.CheckStat[keys[i]], dim_lay_comH[r+i][2])
            lay_comH[r+i].addWidget(QLabel(check_lab[i]), dim_lay_comH[r+i][3])
            self.CheckStat[keys[i]].setStyleSheet("QCheckBox::indicator" \
                               "{" \
                               "width :25px;" \
                               "height : 25px;" \
                               "}")

            lay_comH[r+i].addStretch(dim_lay_comH[r+i][4])

            self.SelStat[keys[i]].setStyleSheet("QComboBox { combobox-popup: 0; }")
            self.SelStat[keys[i]].setMaxVisibleItems(15)
            
        
        r = r+4
        self.Binario = QComboBox()
        self.Binario.addItems(["P","D","P/D","U"])
        lay_comH[r].addWidget(self.Binario, dim_lay_comH[r][0])
        lay_comH[r].addWidget(QLabel("Binario"), dim_lay_comH[r][1])

        self.Alim = QCheckBox()
        self.Alim.setStyleSheet("QCheckBox::indicator" \
                                        "{" \
                                        "width : 25px;" \
                                        "height : 25px;" \
                                        "}")
        lay_comH[r].addWidget(self.Alim, dim_lay_comH[r][2])
        lay_comH[r].addWidget(QLabel("Alimentato"), dim_lay_comH[r][3])

        
        r = r+2
        labels = ["Giorni", "Ora (DA)", "Ora (A)"]

        lay_comTim = QVBoxLayout()
        # Giorni
        lay_singleTim = QHBoxLayout()
        lay_comTim.addLayout(lay_singleTim)
        self.Giorni = QLineEdit()
        lay_singleTim.addWidget(self.Giorni, dim_lay_days[0])
        lay_singleTim.addWidget(QLabel("Giorni"), dim_lay_days[1])
        # Ora_DA
        lay_singleTim = QHBoxLayout()
        lay_comTim.addLayout(lay_singleTim)
        self.OraDa = QSpinBox()
        self.OraDa.setRange(0, 23)
        lay_singleTim.addWidget(self.OraDa, dim_lay_hour[0])
        self.MinDa = QSpinBox()
        self.OraDa.setRange(0, 59)
        lay_singleTim.addWidget(self.MinDa, dim_lay_hour[1])
        lay_singleTim.addWidget(QLabel("Ora (DA)"), dim_lay_hour[2])
        # Ora_A
        lay_singleTim = QHBoxLayout()
        lay_comTim.addLayout(lay_singleTim)
        self.OraA = QSpinBox()
        self.OraA.setRange(0, 23)
        lay_singleTim.addWidget(self.OraA, dim_lay_hour[0])
        self.MinA = QSpinBox()
        self.OraDa.setRange(0, 59)
        lay_singleTim.addWidget(self.MinA, dim_lay_hour[1])
        lay_singleTim.addWidget(QLabel("Ora (A)"), dim_lay_hour[2])
        # Tabella
        lay_comH[r].addLayout(lay_comTim, dim_lay_comH[r][0])
        self.TableDel = QTableWidget(0,1)
        self.TableDel.setHorizontalHeaderLabels(["N ORD"])
        self.TableDel.horizontalHeader().setStretchLastSection(True)
        self.TableDel.cellChanged.connect(self.deleteOrd)
        lay_comH[r].addWidget(self.TableDel, dim_lay_comH[r][1])




        r = r+2
        self.Plot = QPushButton("Grafica")
        lay_comH[r].addWidget(self.Plot, dim_lay_comH[r][0])
        lay_comH[r].addStretch(dim_lay_comH[r][1])
        self.Plot.clicked.connect(self.plotOrd)

        self.Save = QPushButton("Salva")
        lay_comH[r].addWidget(self.Save, dim_lay_comH[r][2])
        lay_comH[r].addStretch(dim_lay_comH[r][3])
        self.Save.clicked.connect(self.saveFile)

        self.setFontSizeWidgets(lay_comV)

        # inizializzazione calendario
        today = datetime.now()
        m = today.month
        y = today.year
        if m == 12:
            m = 1
            y = y+1
        else:
            m = m+1
        
        self.M = m
        self.Y = y
        
        self.Mese.setRange(1,12)
        self.Mese.setValue(m)

        self.Anno.setRange(2000, 3000)
        self.Anno.setValue(y)

        self.setStations() # carico stazioni di default
        self.setCalendar() # carico calendario e plotto tabella

        
        
        # setting finestra principale
        window = QWidget()
        window.setLayout(lay_base)
        self.setCentralWidget(window)
        
        

        
        # testbench
        
        self.SelStat["AMB"].setCurrentIndex(1)
        self.CheckStat["AMB"].setChecked(True)
        self.Giorni.setText("1 3  5 12")
        self.OraDa.setValue(22)
        self.OraA.setValue(4)
        self.Plot.click()
        
        
        self.SelStat["DA"].setCurrentIndex(9)
        self.SelStat["A"].setCurrentIndex(6)
        self.CheckStat["AMB"].setChecked(False)
        self.Giorni.setText("3 6  9 24")
        self.Alim.setChecked(False)
        self.CheckStat["DA"].setChecked(True)
        self.OraDa.setValue(22)
        self.OraA.setValue(4)
        self.Plot.click()
        
        self.nOrd.setValue(5)
        self.SelStat["DA"].setCurrentIndex(16)
        self.SelStat["A"].setCurrentIndex(3)
        self.CheckStat["AMB"].setChecked(False)
        self.Giorni.setText("4 8")
        self.Alim.setChecked(True)
        self.CheckStat["A"].setChecked(True)
        self.OraDa.setValue(22)
        self.MinDa.setValue(30)
        self.OraA.setValue(7)
        self.MinA.setValue(20)
        self.Plot.click()

        self.nOrd.setValue(5)
        self.SelStat["AMB"].setCurrentIndex(16)
        self.CheckStat["AMB"].setChecked(True)
        self.Giorni.setText("5 10")
        self.Alim.setChecked(True)
        self.OraDa.setValue(22)
        self.MinDa.setValue(30)
        self.OraA.setValue(7)
        self.MinA.setValue(20)
        self.Plot.click()

        self.Save.click()
        
        
        """
        self.Riprogram.click()
        """

    def setFontSizeWidgets(self, layout):
        for i in range(layout.count()):
            item = layout.itemAt(i)

            if isinstance(item, QWidgetItem):
                widget = item.widget()

                font = widget.font()
                font.setPointSize(self.fontSize)  # Adjust the font size as needed
                widget.setFont(font)

                widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            elif isinstance(item, QSpacerItem):
                # Handle QSpacerItem if needed
                pass

            elif isinstance(item.layout(), QBoxLayout):
                # Recursively handle nested layout
                self.setFontSizeWidgets(item.layout())

    # startup function load the data of next month
    def setCalendar(self):
        m = self.Mese.value()
        self.M = m
        y = self.Anno.value()
        self.Y = y


        cal = calendar.Calendar()
        self.Cal = cal.monthdayscalendar(y, m)
        # bisogna aggiungere un giorno in più se l'ultimo giorno ultima settima
        if self.Cal[-1][-1] != 0:
            self.Cal.append([1, 0, 0, 0, 0, 0, 0])
        else:
            ind = self.Cal[-1].index(0) # aggiungo 1 del mese successivo
            self.Cal[-1][ind] = 1

        self.refreshTable() # riplot della tabella
        
        # va fatta la disconnessione
        try: self.SelWeek.currentIndexChanged.disconnect()
        except Exception: pass
        self.SelWeek.clear()
        # aggiungere le settimane al ComboBox
        for i in range(len(self.Cal)):
            self.SelWeek.addItem(str(i+1), userData=i)
        # lanciare signal
        self.SelWeek.currentIndexChanged.connect(self.changeWeek)

    def setStations(self, file = "", modify=False):
        if not file and not modify: # se no file e no riprogram allora fiel di deault
            modify = False
            self.nameStatGroup = "Torino Nodo"
            filename = os.path.join(self.workFold, self.nameStatGroup+".txt")
            file = open(filename, "r")


        # LinStat organizzato come mappa {n_linea: {n_stazione: {"name": <name>, "pos": 
                # <indice alto-sinistra print su Panel>}}}
        self.LinStat = {}

        end = False
        i_lin = 0
        prog_num = 0
        line = file.readline()
        while not end:
            line = line.rstrip()
            if line: # ci potrebbe essere una riga vuota
                if line[0] == "#":
                    name_lin = line[1:]
                    i_lin = i_lin+1
                    i_stat = 1
                    self.LinStat[i_lin] = {0: {"name": "---"+name_lin+"---", "pos": prog_num}}
                    prog_num = prog_num+1
                else:
                    name_stat = line
                    self.LinStat[i_lin][i_stat] =  {"name": name_stat, "pos": prog_num}
                    i_stat = i_stat+1
                    prog_num = prog_num+1

            line = file.readline()

            if (not modify and not line) or \
                (modify and line == "####\n"):
                end = True

        # disconnessione del Slot
        try: self.SelStat["DA"].currentIndexChanged.disconnect()
        except Exception: pass
        # set il combo
        for lab in ["AMB", "DA", "A"]:
            self.setComboStations(lab, 0)
        # signal per DA ComboBox
        self.SelStat["DA"].currentIndexChanged.connect(self.selToStat)
            
        if not modify:
            file.close()
        else:
            return file

    def setComboStations(self, name, i_lin):
        # aggiorno le stazioni nel ComboBox "name"
        self.SelStat[name].clear()

        # se i_lin == 0 metto tutte le stazioni altrimenti solo la linea d'interesse
        if i_lin == 0:
            range_lin = self.LinStat.keys()
        else:
            range_lin = [i_lin]

        for i_lin in range_lin:
            for i_stat in self.LinStat[i_lin].keys():
                text = self.LinStat[i_lin][i_stat]["name"]
                self.SelStat[name].addItem(text, userData=[i_lin, i_stat])

    def changeStations(self):
        filename = QFileDialog.getOpenFileName(self, "Scegli File", self.workFold, "Text Files (*.txt);;All Files (*)")
        filename = filename[0]

        self.nameStatGroup, _ext = os.path.splitext(os.path.basename(filename))
        file = open(filename, "r")

        self.setStations(file, False)
        self.refreshTable()

    def refreshTable(self):
        # se cambio periodo elimino dati e plotto tabella
        self.TableDel.clearContents()
        self.TableDel.setRowCount(0)
        self.TableOrd = {}
        self.nOrd.setValue(1)
        self.Panel.printTable(self.Cal, self.LinStat)
        

    
    ########## SIGNALS ##########
    def changeWeek(self):
        i = self.SelWeek.currentData()
        self.Panel.changeWeek(i)

    def selToStat(self):
        i = self.SelStat["DA"].currentData()
        i_lin = i[0]
        self.setComboStations("A", i_lin)

    def showOrdData(self, n_ord):
        n_ord = str(n_ord)
        if n_ord in self.TableOrd:
            self.fillOrdData(n_ord)
        else:
            self.clearOrdData()

    def plotOrd(self):
        data_Ord = {}
        # lettura dati
        n_ord_num = self.nOrd.value()
        n_ord = str(n_ord_num)

        pos_Stat = {}
        check_stat = {}
        labs = ["AMB", "DA", "A"]
        for lab in labs:
            indx = self.SelStat[lab].currentIndex()
            [i_lin, i_stat]  = self.SelStat[lab].currentData()
            pos_Stat[lab] = self.LinStat[i_lin][i_stat]["pos"]
            check_stat[lab] = self.CheckStat[lab].isChecked()
            data_Ord[lab] = [indx, int(check_stat[lab])]

            if lab == "AMB": # salvo eventuale testo addizionale
                if self.LinStat[i_lin][0]["name"] == "---storica---" and \
                    self.LinStat[i_lin][i_stat]["name"] == "TO POR NUOVA":
                    text_add = "\n(11-20)"
                elif self.LinStat[i_lin][0]["name"] == "---genova---" and \
                    self.LinStat[i_lin][i_stat]["name"] == "TO POR NUOVA":
                    text_add = "\n(1-10)"
                else:
                    text_add = ""


        bin = self.Binario.currentText()
        data_Ord["bin"] = self.Binario.currentIndex()

        alim = self.Alim.isChecked()
        data_Ord["al"] = int(alim)
        if alim:
            pen = QPen(Qt.red)
        else:
            pen = QPen(Qt.green)
        pen.setWidth(2)   

        days = self.Giorni.text()
        days = days.split()
        days = [int(day) for day in days if day] # rimuovo elementi nulli e converto in interi
        data_Ord["days"] = days

        h_da = self.OraDa.value()
        min_da = self.MinDa.value()
        
        h_a = self.OraA.value()
        min_a = self.MinA.value()
        
        data_Ord["hour"] = [h_da, min_da, h_a, min_a]

        h_da = h_da + min_da/60
        h_a = h_a +min_a/60


        # elaborazione giorni
        pos_days = []
        for day in days:
            for i_w in range(len(self.Cal)):
                if day in self.Cal[i_w]:
                    i_d = self.Cal[i_w].index(day) # inizio da 1 per ragioni di griglia plot
                    pos_days.append([i_w, i_d]) # salvo per ogni giorni settimana e giorno
                    break 
        
        # elaborazione larghezza da giorni
        pos_x = []
        for pos_day in pos_days:
            i_w, i_d = pos_day
            pos_x_min = i_d+h_da/24
            pos_x_max = i_d+h_a/24 if h_a > h_da else i_d+1+h_a/24
            if pos_x_max <= 7: # se supero 7 finisco in settimana prossima
                pos_x.append([i_w, pos_x_min, pos_x_max])
            else:
                pos_x.append([i_w, pos_x_min, 7])
                pos_x.append([i_w+1, 0, pos_x_max-7])

        if n_ord in self.TableOrd: # potrei avere più plot per la stessa nOrd
            letters = list(string.ascii_lowercase)
            i = 1
            n_ord = n_ord+letters[i]
            while n_ord in self.TableOrd:
                n_ord = n_ord[:-1]+letters[i]
                i += 1

        # elaborazione spessore
        data_Ord["graph"] = {}
        if check_stat["AMB"]:
            text = n_ord+text_add
            pos_y = pos_Stat["AMB"]
            self.Panel.printIntSt(pos_x, pos_y, pen, text, data_Ord["graph"])
        else:
            text = n_ord+"\n"+bin
            pos_y = [pos_Stat["DA"], pos_Stat["A"]]
            self.Panel.printIntLin(pos_x, pos_y, pen, text, data_Ord["graph"])


            pos_y = [pos_Stat["DA"], pos_Stat["A"]]
            if check_stat["DA"]:
                self.Panel.printIntIncl(pos_x, pos_y, pen, "DA", data_Ord["graph"])
            if check_stat["A"]:
                self.Panel.printIntIncl(pos_x, pos_y, pen, "A", data_Ord["graph"])

        
        
        self.TableOrd[n_ord] = data_Ord

        # table for deleting
        row = self.TableDel.rowCount()
        self.TableDel.insertRow(row)
        n_ord = QTableWidgetItem(n_ord)
        n_ord.setFlags(n_ord.flags() & ~Qt.ItemIsEditable)
        n_ord.setFlags(n_ord.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        n_ord.setCheckState(Qt.Checked)

        self.TableDel.setItem(row, 0, n_ord)

        # incremento numero ordinata
        self.nOrd.setValue(n_ord_num+1)

    def deleteOrd(self, row, col):
        item = self.TableDel.item(row, col)
        if item.checkState() == Qt.Unchecked:
            n_ord = item.text()
            self.TableDel.removeRow(row)

            graphics = self.TableOrd[n_ord]["graph"]
            self.Panel.removeInt(graphics)

            # n_ord potrebbe contenere lettere se duplicato
            n_ord_num = n_ord[:-1] if n_ord[-1].isalpha() else n_ord
            self.nOrd.setValue(int(n_ord_num))

            self.fillOrdData(n_ord)

            self.TableOrd.pop(n_ord, None)


    def fillOrdData(self, n_ord):
        # riscrivo i valori
        data_Ord = self.TableOrd[n_ord]
        for lab in ["AMB", "DA", "A"]:
            self.SelStat[lab].setCurrentIndex(data_Ord[lab][0])
            self.CheckStat[lab].setChecked(bool(data_Ord[lab][1]))
        
        self.Binario.setCurrentIndex(data_Ord["bin"])
        self.Alim.setChecked(bool(data_Ord["al"]))

        days = data_Ord["days"]
        days = [str(day) for day in days]
        days = " ".join(days)
        self.Giorni.setText(days)

        h_da, min_da, h_a, min_a = data_Ord["hour"]
        self.OraDa.setValue(h_da)
        self.MinDa.setValue(min_da)
        self.OraA.setValue(h_a)
        self.MinA.setValue(min_a)

    def clearOrdData(self):
        labs = ["AMB", "DA", "A"]
        for lab in labs:
            self.SelStat[lab].setCurrentIndex(0)
            self.CheckStat[lab].setChecked(False)

        self.Binario.setCurrentIndex(0)

        self.Alim.setChecked(False)

        self.Giorni.setText("")


        self.OraDa.setValue(0)
        self.MinDa.setValue(0)
        self.OraA.setValue(0)
        self.MinA.setValue(0)




    def saveFile(self):
        y = str(self.Anno.value())
        m = str(self.Mese.value())
        folder = os.path.join(self.workFold, y+ "_"+ m + " " + self.nameStatGroup)
        if not os.path.exists(folder):
            os.makedirs(folder)
        filename = os.path.join(folder, "Save_"+y+ "_"+ m + ".txt")
        file = open(filename, 'w')

        file.write(m+","+y+"\n")
        file.write(self.nameStatGroup+"\n")
        # salva stazioni
        for i_lin in self.LinStat.keys():
            for i_stat in self.LinStat[i_lin].keys():
                if i_stat == 0: # salvo nome linea
                    name_lin = self.LinStat[i_lin][0]["name"]
                    name_lin = name_lin[3:-3] # rimuovo i segni ---<>---
                    file.write("#"+name_lin+"\n")
                else: #salvo nome stazione
                    file.write(self.LinStat[i_lin][i_stat]["name"]+"\n")
        file.write("####\n")
        # salva dati
        labs = ["AMB", "DA", "A"]
        for n_ord in self.TableOrd.keys():
            
            n_ord_write = n_ord[:-1] if n_ord[-1].isalpha() else n_ord

            file.write(n_ord_write+",")
            for lab in labs:
                st_data = self.TableOrd[n_ord][lab]
                for data in st_data: # i=0: index of ComboBox, i=1: CheckedBox
                    file.write(str(data)+",")
            file.write(str(self.TableOrd[n_ord]["bin"])+",") # index binario ComboBox
            file.write(str(self.TableOrd[n_ord]["al"])+",") # 0-1 in base ad alimentazione

            for d in self.TableOrd[n_ord]["days"]:
                file.write(str(d)+" ")
            for h in self.TableOrd[n_ord]["hour"]:
                file.write(","+str(h))

            file.write("\n")

        self.Panel.print2PDF(folder, self.M, self.Y)

    def loadFile(self):

        filename = QFileDialog.getOpenFileName(self, "Scegli File", self.workFold, "Text Files (*.txt);;All Files (*)")
        filename = filename[0]
        file = open(filename, "r")

        line = file.readline() # carico calendario
        line = line.strip()
        cal = line.split(",")
        self.M = int(cal[0])
        self.Mese.setValue(self.M)
        self.Y = int(cal[1])
        self.Anno.setValue(self.Y)
        
        self.setCalendar()

        line = file.readline() # carico nome gruppo stazioni
        self.nameStatGroup = line.strip()
        self.setStations(file, True) # carico stazioni

        self.Panel.printTable(self.Cal, self.LinStat) # print della tabella

        line = file.readline()
        while line:
            line = line.strip()
            data = line.split(",")
            i = 0
            self.nOrd.setValue(int(data[i]))
            i += 1
            for lab in ["AMB", "DA", "A"]:
                self.SelStat[lab].setCurrentIndex(int(data[i]))
                i += 1
                self.CheckStat[lab].setChecked(bool(int(data[i])))
                i += 1

            self.Binario.setCurrentIndex(int(data[i]))
            i += 1
            self.Alim.setChecked(bool(int(data[i])))
            i += 1

            self.Giorni.setText(data[i])
            i += 1
            self.OraDa.setValue(int(data[i]))
            i += 1
            self.MinDa.setValue(int(data[i]))
            i += 1
            self.OraA.setValue(int(data[i]))
            i += 1
            self.MinA.setValue(int(data[i]))
            
            self.plotOrd()

            line = file.readline()

        


            
            






        

        


        
            


            



        

    

        
            
            



        



