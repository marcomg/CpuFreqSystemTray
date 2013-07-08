#!/usr/bin/python
#############################################################################
#    Copyright (C) 2007 by Arturo Mann                                      #
#    arturo.mann@gmail.com                                                  #
#                                                                           #
#    Copyright (C) 2013 by Marco Guerrini                                   #
#    marcomg@cryptolab.net                                                  #
#                                                                           #
#    Thanks to Michael Andreas Buchberger for adding Conservative mode      #
#                                                                           #
#    This program is free software: you can redistribute it and/or modify   #
#    it under the terms of the GNU General Public License as published by   #
#    the Free Software Foundation, either version 3 of the License, or      #
#    (at your option) any later version.                                    #
#                                                                           #
#    This program is distributed in the hope that it will be useful,        #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
#    GNU General Public License for more details.                           #
#                                                                           #
#    You should have received a copy of the GNU General Public License      #
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#############################################################################

# Cpufreqtray: A graphical manager for cpufreq-set.
import subprocess;
import sys;
import os;
from PyQt4 import QtGui;
from PyQt4 import QtCore;
# -- Check current processor state:
def checkCurrentState():
    CheckState = subprocess.Popen(['cpufreq-info -p'],shell=True, stdout=subprocess.PIPE);
    data = CheckState.stdout.read(128);
    governor = str(data.split(" ")[2])[:-1];
    # -- Switch State:
    if governor == "ondemand":
        CpuFreqIcon.setIcon(DemandIcon);
        CpuFreqIcon.setToolTip("CpuFreqTray: Current Governor: On Demand.");
    if governor == "performance":
        CpuFreqIcon.setIcon(PerfIcon);
        CpuFreqIcon.setToolTip("CpuFreqTray: Current Governor: Performance.");
    if governor == "powersave":
        CpuFreqIcon.setIcon(SaveIcon);
        CpuFreqIcon.setToolTip("CpuFreqTray: Current Governor: Powersave.");
    if governor == "conservative":
        CpuFreqIcon.setIcon(ConsIcon);
        CpuFreqIcon.setToolTip("CpuFreqTray: Current Governor: Conservative.");
        
# -- Set Conservative Governor: 
def setCons():
    setState = subprocess.Popen(['pkexec cpufreq-set -r -g conservative'],shell=True);
    checkCurrentState();
    
# -- Set Performance governor:
def setPerformance():
    setState = subprocess.Popen(['pkexec cpufreq-set -r -g performance'],shell=True);
    checkCurrentState();
    
# -- Set Powersave Governor:
def setSave():
    setState = subprocess.Popen(['pkexec cpufreq-set -r -g powersave'],shell=True);
    checkCurrentState();
    
# -- Set OnDemand Governor: 
def setDemand():
    setState = subprocess.Popen(['pkexec cpufreq-set -r -g ondemand'],shell=True);
    checkCurrentState();
    
    
# -- Main App Glue:    
def main():
    #-- construct the core objects:
    global CpuFreqApp;
    global CpuFreqIcon;
    CpuFreqApp = QtGui.QApplication(sys.argv);
    CpuFreqIcon = QtGui.QSystemTrayIcon();
    Timer = QtCore.QTimer();
    
    # -- create the icons:
    global ConsIcon;
    global PerfIcon;
    global DemandIcon;
    global SaveIcon;
    PerfIcon = QtGui.QIcon("performance.png");
    SaveIcon  = QtGui.QIcon("powersave.png");
    DemandIcon = QtGui.QIcon("ondemand.png");
    ConsIcon = QtGui.QIcon("conservative.png");
    QuitIcon = QtGui.QIcon("quit.png");
    # -- Now Create the menu
    global ActionsMenu;
    ActionsMenu = QtGui.QMenu();
    ConsAction = ActionsMenu.addAction(ConsIcon,"Set governor to Conservative");
    PerfAction = ActionsMenu.addAction(PerfIcon,"Set governor to Performance");
    SaveAction = ActionsMenu.addAction(SaveIcon,"Set governor to Powersave");
    DemandAction = ActionsMenu.addAction(DemandIcon,"Set governor to On Demand");
    ActionsMenu.addSeparator();
    QuitAction = ActionsMenu.addAction(QuitIcon,"Quit CpuFreqTray");
    # -- connect the actions:
    CpuFreqApp.connect(ConsAction,QtCore.SIGNAL("triggered()"),setCons);
    CpuFreqApp.connect(PerfAction,QtCore.SIGNAL("triggered()"),setPerformance);
    CpuFreqApp.connect(DemandAction,QtCore.SIGNAL("triggered()"),setDemand);
    CpuFreqApp.connect(SaveAction,QtCore.SIGNAL("triggered()"),setSave);
    CpuFreqApp.connect(QuitAction,QtCore.SIGNAL("triggered()"),CpuFreqApp.exit);
    CpuFreqApp.connect(Timer,QtCore.SIGNAL("timeout()"),checkCurrentState);
    # -- Now add the menu:
    # -- trigger the check action to set current state
    checkCurrentState();
    CpuFreqIcon.setContextMenu(ActionsMenu);
    CpuFreqIcon.show();
    Timer.start(3000);
    CpuFreqApp.exec_();
    
main();