from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtWidgets import *
from .UI_Drastic_window import Ui_Drastic_window
from .Depth_groundwater import Depth_groundwater
from .Recharge import Recharge
from .Aquifer_media import Aquifer_media
from .Soil_media import Soil_media
from .Topography import Topography
from .Impact_zone import Impact_zone
from .Hidraulic_conductivity import Hidraulic_conductivity
from .Drastic import Drastic
from .Groundwater import Groundwater
from .Overall import Overall
from .Depth import Depth
from .God import God
from .DGroundwater import DGroundwater
from .AnnualRecharge import AnnualRecharge
from .AquiferLithology import AquiferLithology
from .Topogra import Topogra
from .Soggicenza import Soggicenza
from .Infiltrazione import Infiltrazione
from .NoSaturo import NoSaturo
from .Tipologia import Tipologia
from .Acquifero import Acquifero
from .conducibilita import Conducibilita
from .Superficie_topografica import Superficie_topografica
from .SINTACS import SINTACS
from .LU import LU
from .SI import SI
from .analysis import analysis
from .stats import stats
from .simb import simb

try:
    from qgis.PyQt.QtCore import QString
except ImportError:
    QString = str

class Drastic_window(QMainWindow, Ui_Drastic_window):
    
    def __init__(self, iface):
        QMainWindow.__init__(self)  
        self.iface = iface
        self.setupUi(self)
        self.setWindowTitle("GVTool")
        #self.process = QProcess(self) 
        
        self.canvas = QgsMapCanvas()
        self.canvas.setCanvasColor(QColor(255,255,255))
        self.setCentralWidget(self.canvas)
       
       
        actionMenuFile = self.menuBar.addMenu(self.menuFile)
        actionMenuDrastic = self.menuBar.addMenu(self.menuDrastic)
        actionMenuGod = self.menuBar.addMenu(self.menuGod)
        actionMenuSI = self.menuBar.addMenu(self.menuSI)
        actionMenuSINTACS = self.menuBar.addMenu(self.menuSINTACS)
        actionMenuAnalysis = self.menuBar.addMenu(self.menuAnalysis)
        actionMenuStats = self.menuBar.addMenu(self.menuStats)
        actionMenuSimb = self.menuBar.addMenu(self.menuSimb)
        actionMenuHelp = self.menuBar.addMenu(self.menuHelp)
       
        
        # connect help to help window
        actionMenuHelp.triggered.connect(self.helpRequested)
        
        
        # actions for DRASTIC menu
        self.actionDepth_groundwater = self.menuDrastic.addAction(QIcon(), self.tr("Depth to Groundwater (D)"), self.doDepth_groundwater, QKeySequence("F1"))
        self.actionRecharge = self.menuDrastic.addAction(QIcon(""), self.tr("Net Recharge (R)"), self.doRecharge, QKeySequence("F2"))
        self.actionAquifer = self.menuDrastic.addAction(QIcon(""), self.tr("Aquifer Media (A)"), self.doAquifer_media, QKeySequence("F3"))
        self.actionSoil = self.menuDrastic.addAction(QIcon(""), self.tr("Soil Media (S)"), self.doSoil_media, QKeySequence("F4"))
        self.actionTopography = self.menuDrastic.addAction(QIcon(""), self.tr("Topography (T)"), self.doTopography, QKeySequence("F5"))
        self.actionImpact = self.menuDrastic.addAction(QIcon(""), self.tr("Impact of the Vadose Zone (I)"), self.doImpact_zone, QKeySequence("F6"))
        self.actionHidraConduc = self.menuDrastic.addAction(QIcon(""), self.tr("Hydraulic Conductivity (C)"), self.doHidraulic_conductivity, QKeySequence("F7"))
        self.actionDrastic = self.menuDrastic.addAction(QIcon(""), self.tr("DRASTIC"), self.doDrastic, QKeySequence("F8"))
        
        # actions for GOD menu
        self.actionGroundwater = self.menuGod.addAction(QIcon(""), self.tr("Groundwater Occurrence (G)"), self.doGroundwater, QKeySequence("F1"))
        self.actionOverall = self.menuGod.addAction(QIcon(""), self.tr("Overall lithology of aquifer or aquitard (O)"), self.doOverall, QKeySequence("F2"))
        self.actionDepth = self.menuGod.addAction(QIcon(""), self.tr("Depth to Groundwater (D)"), self.doDepth, QKeySequence("F3"))
        self.actionGOD = self.menuGod.addAction(QIcon(""), self.tr("GOD"), self.doGod, QKeySequence("F3"))
        
        # actions for SI menu
        self.actionDGroundwater = self.menuSI.addAction(QIcon(""), self.tr("Depth to Groundwater (G)"), self.doDGroundwater, QKeySequence("F1"))
        self.actionAnnualRecharge = self.menuSI.addAction(QIcon(""), self.tr("Annual Recharge (R)"), self.doAnnualRecharge, QKeySequence("F2"))
        self.actionAquiferLithology = self.menuSI.addAction(QIcon(""), self.tr("Aquifer Lithology (A)"), self.doAquiferLithology, QKeySequence("F3"))
        self.actionTopogra = self.menuSI.addAction(QIcon(""), self.tr("Topography (T)"), self.doTopogra, QKeySequence("F3"))
        self.actionLU = self.menuSI.addAction(QIcon(""), self.tr("Land Use (LU)"), self.doLU, QKeySequence("F3"))
        self.actionSI = self.menuSI.addAction(QIcon(""), self.tr("Susceptibility Index"), self.doSI, QKeySequence("F3"))
        
        # actions for File menu
        self.actionAddRasterLayer = self.menuFile.addAction(QIcon(":/plugins/DRASTIC/calc.png"), self.tr("Add Raster Layer"), self.AddRaster, QKeySequence("F1"))
        self.actionAddVectorLayer = self.menuFile.addAction(QIcon(":/plugins/DRASTIC/raster.png"), self.tr("Add Vector Layer"), self.AddVector, QKeySequence("F2"))

        # actions for SINTACS menu
        self.actionSoggicenza = self.menuSINTACS.addAction(QIcon(":/plugins/DRASTIC/s.png"),
                                                                  self.tr("Soggicenza - Depth to groundwater (S)"),
                                                                  self.doSoggicenza, QKeySequence("F1"))
        self.actionInfiltrazione = self.menuSINTACS.addAction(QIcon(":/plugins/DRASTIC/i.png"),
                                                        self.tr("Infiltrazione - Effective Infiltration (I)"), self.doInfiltrazione,
                                                      QKeySequence("F2"))
        self.actionNonSaturo = self.menuSINTACS.addAction(QIcon(":/plugins/DRASTIC/n.png"),
                                                        self.tr("No Saturo - Unsatured Zone Attenuation Capacity (N)"), self.doNoSaturo,QKeySequence("F3"))
        self.actionTipologia = self.menuSINTACS.addAction(QIcon(":/plugins/DRASTIC/t.png"), self.tr("Tipologia della copertura - Soil /Overburden Attenuation Capacity (T)"),
                                                      self.doTipologia, QKeySequence("F4"))
        self.actionAcquifero = self.menuSINTACS.addAction(QIcon(":/plugins/DRASTIC/a.png"),
                                                          self.tr("Acquifero - Satured Zone Features (A)"), self.doAcquifero,
                                                         QKeySequence("F5"))
        self.actionConducibilita = self.menuSINTACS.addAction(QIcon(":/plugins/DRASTIC/c.png"),
                                                        self.tr("Conducibilita - Hydraulic Conductivity (C)"), self.doConducibilita,
                                                        QKeySequence("F6"))
        self.actionSuperficie = self.menuSINTACS.addAction(QIcon(":/plugins/DRASTIC/s.png"),
                                                            self.tr("Superficie Topografica - Topographic Surface Slope (S)"),
                                                            self.doSuperficie, QKeySequence("F7"))
        self.actionSINTACS = self.menuSINTACS.addAction(QIcon(":/plugins/DRASTIC/sintacs.png"), self.tr("SINTACS"),
                                                        self.doSintacs, QKeySequence("F8"))

        # actions for Analysis menu
        self.actionComparativeAnalysis = self.menuAnalysis.addAction(QIcon(":/plugins/DRASTIC/sintacs.png"),
                                                                     self.tr("Comparative Analysis"), self.doAnalysis)

        # actions for STATS menu
        self.actionStats = self.menuStats.addAction(QIcon(":/plugins/DRASTIC/sintacs.png"),
                                                                     self.tr("Map Statistics"), self.doStats)

        #actions for SIMB menu
        self.actionSimb = self.menuSimb.addAction(QIcon(":/plugins/DRASTIC/sintacs.png"),
                                                    self.tr("Apply Symbology"), self.doSimb)

    def unload(self):
        self.menu.removeAction(self.Drastic_menu.menuAction())  
  
    def doDGroundwater(self):
        self.dlgDGroundwater = DGroundwater(self)
        if DGroundwater ==0:
            return
        self.dlgDGroundwater.show()
        self.dlgDGroundwater.exec_() 
    
    def doAnnualRecharge(self):
        self.dlgAnnualRecharge = AnnualRecharge(self)
        if AnnualRecharge ==0:
            return
        self.dlgAnnualRecharge.show()
        self.dlgAnnualRecharge.exec_()  
        
    def doAquiferLithology(self):
        self.dlgAquiferLithology = AquiferLithology(self)
        if AquiferLithology ==0:
            return
        self.dlgAquiferLithology.show()
        self.dlgAquiferLithology.exec_()  
        
    def doTopogra(self):
        self.dlgTopogra = Topogra(self)
        if Topogra ==0:
            return
        self.dlgTopogra.show()
        self.dlgTopogra.exec_()  
        
    def doLU(self):
        self.dlgLU = LU(self)
        if LU ==0:
            return
        self.dlgLU.show()
        self.dlgLU.exec_()  
        
    def doSI(self):
        self.dlgSI = SI(self)
        if SI ==0:
            return
        self.dlgSI.show()
        self.dlgSI.exec_()  
    
    def doGroundwater(self):
        self.dlgGroundwater = Groundwater(self)
        if Groundwater ==0:
            return
        self.dlgGroundwater.show()
        self.dlgGroundwater.exec_()   
        
    def doGod(self):
        self.dlgGod = God(self)
        if God ==0:
            return
        self.dlgGod.show()
        self.dlgGod.exec_()      
        
    def doOverall(self):
        self.dlgOverall = Overall(self)
        if Overall ==0:
            return
        self.dlgOverall.show()
        self.dlgOverall.exec_()      
        
    def doDepth(self):
        self.dlgDepthG = Depth(self)
        if Depth ==0:
            return
        self.dlgDepthG.show()
        self.dlgDepthG.exec_()    
        
    def doDepth_groundwater(self):
        self.dlgDepth = Depth_groundwater(self)
        if Depth_groundwater ==0:
            return
        self.dlgDepth.show()
        self.dlgDepth.exec_()
        
        
    def doRecharge(self):
        self.dlgRecharge = Recharge(self)
        if Recharge ==0:
            return
        self.dlgRecharge.show()
        self.dlgRecharge.exec_()    
    
    def doAquifer_media(self):
        self.dlgAquifer = Aquifer_media(self)
        if Aquifer_media ==0:
            return
        self.dlgAquifer.show()
        self.dlgAquifer.exec_()   
        
    def doSoil_media(self):
        self.dlgSoil = Soil_media(self)
        if Soil_media ==0:
            return
        self.dlgSoil.show()
        self.dlgSoil.exec_()
        
    def doTopography(self):
        self.dlgTopography = Topography(self)
        if Topography ==0:
            return
        self.dlgTopography.show()
        self.dlgTopography.exec_()    
        
    def doImpact_zone(self):
        self.dlgImpact = Impact_zone(self)
        if Impact_zone ==0:
            return
        self.dlgImpact.show()
        self.dlgImpact.exec_()
    
    def doHidraulic_conductivity(self):
        self.dlgHidraulic = Hidraulic_conductivity(self)
        if Hidraulic_conductivity==0:
            return
        self.dlgHidraulic.show()
        self.dlgHidraulic.exec_()    
        
    def doDrastic(self):
        self.dlgDrastic = Drastic(self)
        if Drastic==0:
            return
        self.dlgDrastic.show()
        self.dlgDrastic.exec_()

    def doSoggicenza(self):
        self.dlgSoggicenza = Soggicenza(self)
        if Soggicenza==0:
            return
        self.dlgSoggicenza.show()
        self.dlgSoggicenza.exec_()

    def doInfiltrazione(self):
        self.dlgInfiltrazione = Infiltrazione(self)
        if Infiltrazione==0:
            return
        self.dlgInfiltrazione.show()
        self.dlgInfiltrazione.exec_()

    def doNoSaturo(self):
        self.dlgNoSaturo = NoSaturo(self)
        if NoSaturo == 0:
            return
        self.dlgNoSaturo.show()
        self.dlgNoSaturo.exec_()

    def doTipologia(self):
        self.dlgTipologia = Tipologia(self)
        if Tipologia == 0:
            return
        self.dlgTipologia.show()
        self.dlgTipologia.exec_()

    def doAcquifero(self):
        self.dlgAcquifero = Acquifero(self)
        if Acquifero == 0:
            return
        self.dlgAcquifero.show()
        self.dlgAcquifero.exec_()

    def doConducibilita(self):
        self.dlgConducibilita = Conducibilita(self)
        if Conducibilita == 0:
            return
        self.dlgConducibilita.show()
        self.dlgConducibilita.exec_()

    def doSuperficie(self):
        self.dlgSuperficie = Superficie_topografica(self)
        if Superficie_topografica == 0:
            return
        self.dlgSuperficie.show()
        self.dlgSuperficie.exec_()

    def doSintacs(self):
        self.dlgSintacs = SINTACS(self)
        if SINTACS == 0:
            return
        self.dlgSintacs.show()
        self.dlgSintacs.exec_()

    def doAnalysis(self):
        self.dlgAnalysis = analysis(self)
        if analysis == 0:
            return
        self.dlgAnalysis.show()
        self.dlgAnalysis.exec_()

    def doStats(self):
        self.dlgStats = stats(self)
        if stats == 0:
            return
        self.dlgStats.show()
        self.dlgStats.exec_()

    def doSimb(self):
        self.dlgSimb = simb(self)
        if simb == 0:
            return
        self.dlgSimb.show()
        self.dlgSimb.exec_()

        
    def AddVector(self):
        file = QFileDialog.getOpenFileName(self, "Open shapefile", ".", "Shp (*.shp)")   
        fileInfo = QFileInfo(file[0])
        
        # add the shapefile
        layer = QgsVectorLayer(file[0], fileInfo.fileName(), "ogr")
        
        if not layer.isValid():
            return
        
        # add layer to the registry
        QgsProject.instance().addMapLayer(layer)
        
        # set extent to the extent of our layer
        self.canvas.setExtent(layer.extent())
        
        # set the map canvas layer set
        self.canvas.setLayers([layer])
        
    def AddRaster(self):
        file = QFileDialog.getOpenFileName(self, "Open raster", ".", "Images(*.tif *.png *.jpg *.jpeg *.img)")
        fileInfo = QFileInfo(file[0])
        
        # add the raster
        layer = QgsRasterLayer(file[0], fileInfo.fileName(), "gdal")
        
        if not layer.isValid():
            return
        
        # add layer to the registry
        QgsProject.instance().addMapLayer(layer)
        
        # set extent to the extent of our layer
        self.canvas.setExtent(layer.extent())
        
        # set the map canvas layer set
        self.canvas.setLayers([layer])
        
    def helpRequested(self):
        QMessageBox.about(self, "Help", """<p>The tool determines the spatial distribution of the DRASTIC index and incorporates some procedures under a plugin. <p>
        <p>The DRASTIC method comprises several factors and the corresponding maps: <p>
        <p><b>Depth to groundwater (D)<b<p>
        <p><b>Net Recharge (R)<b><p>
        <p><b>Aquifer media (A)<b><p>
        <p><b>Soil media (S)<b><p>
        <p><b>Topography (T)<b><p>
        <p><b>Impact of the Vadose Zone (I) <b><p>
        <p><b>Hydraulic Conductivity (C)<b><p>
        
        <p>The application consists of a window where the spatial objects can be presented. <p>
        <p>This window allows the user to analyze the result and modify the input parameters. <p>
        <p>The DRASTIC window is composed by a map canvas, a menu bar containing a <b>File<b> menu, the <b>DRASTIC<b> menu and the <b>Help<b> menu.<p>
        <p>The first one is composed by two buttons that allow the user to add a vector or a raster file (<b>Add Vector File<b> and <b>Add Raster File<b>). <p>
        <p>The DRASTIC menu is composed by eight buttons, one for each factor.<p> """)
        
        
    def ident(self):
        QMessageBox.about(self, "Help", """abc""")
    
