from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import QPrinter
import os

class DrawPanel(QGraphicsView):
    def __init__(self):

        self.dx = 125
        self.dy = 37

        super().__init__()

    def printTable(self, cal, LinStat):
        self.Scene = []
        labels = ["Lunedì", "Martedì", "Mercoledì", \
                "Giovedì", "Venerdì", "Sabato", "Domenica"];
        

        for i_w in range(len(cal)):
            scene = QGraphicsScene()
            for i_x in range(8):
                if i_x > 0:
                    # caselle settimana
                    pen = QPen(Qt.black)
                    pen.setWidth(2)

                    rect = QGraphicsRectItem(i_x*self.dx, 0, self.dx, self.dy)
                    rect.setPen(pen)
                    scene.addItem(rect)

                    text = labels[i_x-1]
                    if cal[i_w][i_x-1] != 0:
                        text += " "+str(cal[i_w][i_x-1])
                    text = QGraphicsTextItem(text)
                    cent_x = rect.rect().center().x()
                    cent_y = rect.rect().center().y()
                    text_dx = text.boundingRect().width()
                    text_dy = text.boundingRect().height()
                    text.setPos(cent_x-text_dx/2, cent_y-text_dy/2)
                    scene.addItem(text)

                pen = QPen(Qt.black)
                pen.setWidth(1)
                for i_lin in LinStat.keys():
                    for i_stat in LinStat[i_lin].keys():
                        if i_stat > 0: # 0 è il nome della linea
                            i_y = LinStat[i_lin][i_stat]["pos"]
                            rect = QGraphicsRectItem(i_x*self.dx, i_y*self.dy, self.dx, self.dy)
                            rect.setPen(pen)
                            scene.addItem(rect)
                            # testo nome stazioni
                            if i_x == 0:
                                text = LinStat[i_lin][i_stat]["name"]
                                text = QGraphicsTextItem(text)
                                cent_x = rect.rect().center().x()
                                cent_y = rect.rect().center().y()
                                text_dx = text.boundingRect().width()
                                text_dy = text.boundingRect().height()
                                text.setPos(cent_x-text_dx/2, cent_y-text_dy/2)
                                scene.addItem(text)
            
            self.Scene.append(scene)

        self.setScene(self.Scene[0])

    def printIntLin(self, Pos_x, Pos_y, pen, label, graph_obj): # plot rettangoli per intterruzione su linea
        graph_obj = {}

        Pos_y.sort()
        pos_y_min, pos_y_max = Pos_y
        pos_y_min += 2/3 # posizione rettangolo rispetto bordo superiore
        pos_y_max += 1/3
        heigth = pos_y_max-pos_y_min



        
        for pos_x in Pos_x:
            i_w, pos_x_min, pos_x_max = pos_x
            pos_x_min += 1 # casella nomi stazioni
            pos_x_max += 1
            width = pos_x_max-pos_x_min

            

            

            rect = QGraphicsRectItem(self.dx*pos_x_min, self.dy*pos_y_min,  \
                                     self.dx*width, self.dy*heigth)
            
            rect.setPen(pen)
            self.Scene[i_w].addItem(rect)
            

            text = QGraphicsTextItem(label)
            cent_x = rect.rect().center().x()
            cent_y = rect.rect().center().y()
            text_dx = text.boundingRect().width()
            text_dy = text.boundingRect().height()
            text.setPos(cent_x-text_dx/2, cent_y-text_dy/2)              
            self.Scene[i_w].addItem(text)

            # graphics object per essere elimnati
            if i_w not in graph_obj:
                graph_obj[i_w] = []
            
            graph_obj[i_w].append(rect)
            graph_obj[i_w].append(text)


    def printIntSt(self, Pos_x, pos_y, pen, label, graph_obj): # plot line per interruzione in stazione
        pos_y = pos_y + 0.5 # posizione rispetto bordo superiore

        for pos_x in Pos_x:
            i_w, pos_x_min, pos_x_max = pos_x
            pos_x_min += 1 # casella nomi stazioni
            pos_x_max += 1

            
            line = QGraphicsLineItem(self.dx*pos_x_min, self.dy*pos_y, \
                                     self.dx*pos_x_max, self.dy*pos_y)

            
            line.setPen(pen)
            self.Scene[i_w].addItem(line)

            if i_w not in graph_obj:
                graph_obj[i_w] = []

            graph_obj[i_w].append(line)

            text = QGraphicsTextItem(label)
            pos_x_end = self.dx*pos_x_max
            pos_y_cent = self.dy*pos_y
            text_dx = text.boundingRect().width()
            text_dy = text.boundingRect().height()
            text.setPos(pos_x_end, pos_y_cent-text_dy/2)                
            self.Scene[i_w].addItem(text)

            graph_obj[i_w].append(text)

    def printIntIncl(self, Pos_x, Pos_y, pen, label, graph_obj): # plot line per interruzione in stazione
        # uso la label per capire se è ambito stazione oppure stazione inclusa
        if label == "DA":
            if Pos_y[0] < Pos_y[1]: # caso normale
                pos_y = Pos_y[0]+5/6
            else: # caso strano
                pos_y = Pos_y[0]+1/6
        else:
            if Pos_y[0] < Pos_y[1]: # caso normale
                pos_y = Pos_y[1]+1/6
            else: # caso strano
                pos_y = Pos_y[1]+5/6


        for pos_x in Pos_x:
            i_w, pos_x_min, pos_x_max = pos_x
            pos_x_min += 1 # casella nomi stazioni
            pos_x_max += 1

            
            line = QGraphicsLineItem(self.dx*pos_x_min, self.dy*pos_y, \
                                     self.dx*pos_x_max, self.dy*pos_y)

            
            line.setPen(pen)
            self.Scene[i_w].addItem(line)

            if i_w not in graph_obj:
                graph_obj[i_w] = []

            graph_obj[i_w].append(line)


        
    def removeInt(self, graph_obj):
        for i_w, graph in graph_obj.items():
            for g in graph:
                self.Scene[i_w].removeItem(g)
    
    def changeWeek(self, i_w):
        super().setScene(self.Scene[i_w])

    def print2PDF(self, folder, m, y):
        for week, scene in enumerate(self.Scene):

            pdf_filename = os.path.join(folder, str(y)+"_"+str(m)+"_"+str(week+1)+".pdf")

            # Create a QPrinter
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(pdf_filename)

            # Create a QPainter
            painter = QPainter(printer)

            # Render the scene onto the printer
            scene.render(painter)

            painter.end()




                            

        
        