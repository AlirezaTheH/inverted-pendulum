# Module level imports
from fuzzy.norm.Min import Min
from fuzzy.norm.AlgebraicProduct import AlgebraicProduct
from fuzzy.norm.EinsteinProduct import EinsteinProduct
from fuzzy.defuzzify.COG import COG
from fuzzy.defuzzify.MaxLeft import MaxLeft
from fuzzy.defuzzify.MaxRight import MaxRight

# Project level imports
from ip import *
from qtip import *
from plot import *


class ControlFrame(QGroupBox):
    """
    This frame shows the application control buttons.
    """

    def __init__(self, *cnf):
        QGroupBox.__init__(self, *cnf)

        self.setTitle("Control:")
        self.go_button = QPushButton("Start", self)
        self.stop_button = QPushButton("Stop", self)
        self.step_button = QPushButton("Step", self)

        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.addWidget(self.go_button, Qt.AlignLeft)
        layout.addWidget(self.stop_button, Qt.AlignLeft)
        layout.addWidget(self.step_button, Qt.AlignLeft)

        self.enable()
        self.show()

    def enable(self):
        self.go_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.step_button.setEnabled(True)

    def disable(self):
        self.go_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.step_button.setEnabled(False)


class RedefineFrame(QGroupBox):
    """
    This frame shows controls to reset and redefine the variables on the
    control.
    """

    def __init__(self, *cnf):
        QGroupBox.__init__(self, *cnf)

        self.setTitle("Reset:")
        self.theta_label = QLabel("Theta: ")
        self.omega_label = QLabel("Omega: ")
        self.x_label = QLabel("Position: ")
        self.v_label = QLabel("Speed: ")
        self.theta_edit = QLineEdit(self)
        self.omega_edit = QLineEdit(self)
        self.x_edit = QLineEdit(self)
        self.v_edit = QLineEdit(self)
        self.redef_button = QPushButton("Reset", self)

        layout = QGridLayout(self)
        layout.setSpacing(0)
        layout.addWidget(self.theta_label, 0, 0, 1, 1)
        layout.addWidget(self.omega_label, 1, 0, 1, 1)
        layout.addWidget(self.x_label, 2, 0, 1, 1)
        layout.addWidget(self.v_label, 3, 0, 1, 1)
        layout.addWidget(self.theta_edit, 0, 1, 1, 1)
        layout.addWidget(self.omega_edit, 1, 1, 1, 1)
        layout.addWidget(self.x_edit, 2, 1, 1, 1)
        layout.addWidget(self.v_edit, 3, 1, 1, 1)
        layout.addWidget(self.redef_button, 4, 0, 1, 2)

        self.enable()
        self.show()

    def enable(self):
        self.theta_edit.setEnabled(True)
        self.omega_edit.setEnabled(True)
        self.x_edit.setEnabled(True)
        self.v_edit.setEnabled(True)
        self.redef_button.setEnabled(True)

    def disable(self):
        self.theta_edit.setEnabled(False)
        self.omega_edit.setEnabled(False)
        self.x_edit.setEnabled(False)
        self.v_edit.setEnabled(False)
        self.redef_button.setEnabled(False)

    def feedback(self, O, w, x, v, F):
        self.theta_edit.setText("%5.2f" % (O * 180. / pi))
        self.omega_edit.setText("%7.4f" % w)
        self.x_edit.setText("%7.4f" % x)
        self.v_edit.setText("%7.4f" % v)

    def get_values(self):
        O = float(self.theta_edit.text()) * pi / 180.
        w = float(self.omega_edit.text())
        x = float(self.x_edit.text())
        v = float(self.v_edit.text())
        return O, w, x, v


class ConfigFrame(QGroupBox):
    """
    This frame shows the redefinitions allowed for the controller. You can
    select different defuzzification and logic operations.
    """

    def __init__(self, *cnf):
        QGroupBox.__init__(self, *cnf)

        self.setTitle("Configuration:")
        self.logic_label = QLabel("Fuzzy Logic:")
        self.logic_combo = QComboBox(self)
        self.logic_combo.addItems(["Min", "Algebraic", "Einstein"])
        self.defuzzy_label = QLabel("Defuzzification:")
        self.defuzzy_combo = QComboBox(self)
        self.defuzzy_combo.addItems(["Center Of Gravity",
                                     "Left Global Maximum",
                                     "Right Global Maximum"])

        layout = QGridLayout(self)
        layout.setSpacing(0)
        layout.addWidget(self.logic_label, 0, 0)
        layout.addWidget(self.logic_combo, 0, 1)
        layout.addWidget(self.defuzzy_label, 2, 0)
        layout.addWidget(self.defuzzy_combo, 2, 1)

        self.enable()
        self.show()

    def enable(self):
        self.logic_combo.setEnabled(True)
        self.defuzzy_combo.setEnabled(True)

    def disable(self):
        self.logic_combo.setEnabled(False)
        self.defuzzy_combo.setEnabled(False)


class IPFrame(QFrame):
    """
    Shows every control and process events.
    """

    def __init__(self, app, *cnf):

        # Pendulum data (MKS units)
        l = 0.5
        m = 0.1
        mc = 0.5
        dt = 0.01
        self.ip = InvertedPendulum(l, m, mc, dt)
        self.pc = PC
        self.running = False
        self.Orange = linspace(-3. * pi / 8., 3. * pi / 8., 100)
        self.wrange = linspace(-9. * pi / 2., 9. * pi / 2., 100)
        self.Frange = linspace(-100, 100, 500)
        self.F = 0.
        self.Otrack = []
        self.wtrack = []
        self.xtrack = []
        self.vtrack = []
        self.Ftrack = []

        # Frame Inicialization
        QFrame.__init__(self, *cnf)
        self.app = app
        self.setWindowTitle("Inverted Pendulum")

        # Graphic Elements
        self.ipview = PendulumView(l, m)
        self.graph = PlotWindow(5)
        self.ctrl_frame = ControlFrame(self)
        self.redef_frame = RedefineFrame(self)
        self.config_frame = ConfigFrame(self)

        # Plots
        self.gframe = QFrame(self)
        self.Ograph = PlotWindow(8, self.gframe)
        self.Ograph.setAxisScale(Qwt.QwtPlot.xBottom, -3 * pi / 8, 3 * pi / 8)
        self.Ograph.setAxisScale(Qwt.QwtPlot.yLeft, -0.1, 1.1)
        self.Ograph.set_curve_color(-1, Qt.black)
        for i in range(7):
            self.Ograph.set_curve_style(i, Qt.DotLine)
        self.wgraph = PlotWindow(6, self.gframe)
        self.wgraph.setAxisScale(Qwt.QwtPlot.xBottom, -9 * pi / 2., 9 * pi / 2.)
        self.wgraph.setAxisScale(Qwt.QwtPlot.yLeft, -0.1, 1.1)
        self.wgraph.set_curve_color(-1, Qt.black)
        for i in range(5):
            self.wgraph.set_curve_style(i, Qt.DotLine)
        self.Fgraph = PlotWindow(12, self.gframe)
        self.Fgraph.setAxisScale(Qwt.QwtPlot.xBottom, -100., 100.)
        self.Fgraph.setAxisScale(Qwt.QwtPlot.yLeft, -0.1, 1.1)
        self.Fgraph.set_curve_color(0, Qt.darkGray)
        self.Fgraph.set_curve_baseline(0, 0.)
        self.Fgraph.set_curve_brush(0, QBrush(Qt.gray, Qt.SolidPattern))
        self.Fgraph.set_curve_color(1, Qt.black)
        self.Fgraph.set_curve_baseline(1, 0.)
        self.Fgraph.set_curve_brush(1, QBrush(Qt.darkGray, Qt.SolidPattern))
        self.Fgraph.set_curve_color(2, Qt.red)
        glayout = QGridLayout(self.gframe)
        glayout.addWidget(self.Ograph, 0, 0)
        glayout.addWidget(self.wgraph, 1, 0)
        glayout.addWidget(self.Fgraph, 0, 1, 2, 1)
        glayout.setRowStretch(0, 1)
        glayout.setRowStretch(1, 1)
        glayout.setColumnStretch(0, 1)
        glayout.setColumnStretch(1, 2)
        self.__draw_O()
        self.__draw_w()
        self.__draw_F()
        self.gframe.setLayout(glayout)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self.ipview, 'Pendulum')
        self.tabs.addTab(self.graph, 'Graphics')
        self.tabs.addTab(self.gframe, 'Membership')

        layout = QGridLayout(self)
        layout.addWidget(self.tabs, 0, 0, 5, 1)
        layout.addWidget(self.ctrl_frame, 0, 1)
        layout.addWidget(self.redef_frame, 1, 1)
        layout.addWidget(self.config_frame, 2, 1)
        layout.setRowStretch(0, 0)
        layout.setRowStretch(1, 0)
        layout.setRowStretch(2, 0)
        layout.setRowStretch(3, 0)
        layout.setRowStretch(4, 1)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 0)
        self.feedback(O=0., w=0., x=0., v=0., F=0.)

        # Connects the events
        self.connect(self.ctrl_frame.go_button, SIGNAL("clicked()"), self.on_go_button)
        self.connect(self.ctrl_frame.stop_button, SIGNAL("clicked()"), self.on_stop_button)
        self.connect(self.ctrl_frame.step_button, SIGNAL("clicked()"), self.on_step_button)
        self.connect(self.redef_frame.redef_button, SIGNAL("clicked()"), self.on_redef_button)
        self.connect(self.config_frame.logic_combo, SIGNAL("currentIndexChanged(int)"), self.on_logic_combo)
        self.connect(self.config_frame.defuzzy_combo, SIGNAL("currentIndexChanged(int)"), self.on_defuzzy_combo)
        self.connect(self.tabs, SIGNAL("currentChanged(int)"), self.on_change_tab)

        # Exibe o frame
        self.set_state(pi / 8., 0., 0., 0., 0.)
        self.show()

    def enable(self):
        self.ctrl_frame.enable()
        self.redef_frame.enable()
        self.config_frame.enable()

    def disable(self):
        self.ctrl_frame.disable()
        self.redef_frame.disable()
        self.config_frame.disable()

    def __draw_O(self):
        x = self.Orange
        self.Ograph.set_multi_data([
            (x, map(self.pc.variables['O'].adjectives['Ovbn'].set,x)),
            (x, map(self.pc.variables['O'].adjectives['Obn'].set, x)),
            (x, map(self.pc.variables['O'].adjectives['Osn'].set, x)),
            (x, map(self.pc.variables['O'].adjectives['Oz'].set, x)),
            (x, map(self.pc.variables['O'].adjectives['Osp'].set, x)),
            (x, map(self.pc.variables['O'].adjectives['Obp'].set, x)),
            (x, map(self.pc.variables['O'].adjectives['Ovbp'].set, x)),
            ([0.], [0.])
        ])

    def __draw_w(self):
        x = self.wrange
        self.wgraph.set_multi_data([
            (x, map(self.pc.variables['w'].adjectives['wbn'].set, x)),
            (x, map(self.pc.variables['w'].adjectives['wsn'].set, x)),
            (x, map(self.pc.variables['w'].adjectives['wz'].set, x)),
            (x, map(self.pc.variables['w'].adjectives['wsp'].set, x)),
            (x, map(self.pc.variables['w'].adjectives['wbp'].set, x)),
            ([0.], [0.])
        ])

    def __draw_F(self):
        x = self.Frange
        self.Fgraph.set_multi_data([
            ([0.], [0.]),
            ([0.], [0.]),
            ([0., 0.], [-0.025, -0.1]),
            (x, map(self.pc.variables['F'].adjectives['Fvvbn'].set, x)),
            (x, map(self.pc.variables['F'].adjectives['Fvbn'].set, x)),
            (x, map(self.pc.variables['F'].adjectives['Fbn'].set, x)),
            (x, map(self.pc.variables['F'].adjectives['Fsn'].set, x)),
            (x, map(self.pc.variables['F'].adjectives['Fz'].set, x)),
            (x, map(self.pc.variables['F'].adjectives['Fsp'].set, x)),
            (x, map(self.pc.variables['F'].adjectives['Fbp'].set, x)),
            (x, map(self.pc.variables['F'].adjectives['Fvbp'].set, x)),
            (x, map(self.pc.variables['F'].adjectives['Fvvbp'].set, x))
        ])

    def set_state(self, O, w, x, v, F):
        self.Otrack = [O]
        self.wtrack = [w]
        self.xtrack = [x]
        self.vtrack = [v]
        self.Ftrack = [F]
        self.ip.set_state(O, w, x, v)
        self.feedback(O, w, x, v, F)

    def feedback(self, O, w, x, v, F):
        ci = self.tabs.currentIndex()
        if ci == 0:  # Pendulum
            self.ipview.set_state(O, w, x, v, F)
        elif ci == 1:  # Plots
            t = arange(0., 2.5, self.ip.dt)
            self.graph.set_multi_data([
                (t, self.Otrack), (t, self.wtrack),
                (t, self.xtrack), (t, self.vtrack),
                (t, zeros(t.shape))  # self.Ftrack)
            ])
        elif ci == 2:  # Membership
            self.Ograph.setData(-1, [O, O], [0., 1.])
            self.wgraph.setData(-1, [w, w], [0., 1.])
            self.Fgraph.setData(2, [F, F], [-0.025, -0.1])
        self.redef_frame.feedback(O, w, x, v, F)

    def step(self):
        O, w, x, v = self.ip.get_state()
        F = self.pc({'O': O, 'w': w}, {'F': 0.0})
        self.ip.apply(F)
        self.feedback(O, w, x, v, F)
        self.Otrack.append(O)
        self.wtrack.append(w)
        self.xtrack.append(x)
        self.vtrack.append(v)
        self.Ftrack.append(F)

    def on_go_button(self):
        self.disable()
        self.running = True
        while self.running:
            self.step()
            self.app.processEvents()
        self.enable()

    def on_stop_button(self):
        self.running = False

    def on_step_button(self):
        if self.running:
            return
        self.step()

    def on_redef_button(self):
        if self.running:
            return
        O, w, x, v = self.redef_frame.get_values()
        self.Otrack = []
        self.wtrack = []
        self.xtrack = []
        self.vtrack = []
        self.Ftrack = []
        self.set_state(O, w, x, v, 0)

    def on_logic_combo(self, index):
        if index == 0:
            self.pc.set_norm(Min)
        elif index == 1:
            self.pc.set_norm(AlgebraicProduct)
        elif index == 2:
            self.pc.set_norm(EinsteinProduct)

    def on_defuzzy_combo(self, index):
        if index == 0:     # Center Of Gravity
            self.pc.set_defuzzy(COG)
        elif index == 1:   # Left Global Maximum
            self.pc.set_defuzzy(MaxLeft)
        elif index == 2:   # Right Global Maximum
            self.pc.set_defuzzy(MaxRight)

    def on_change_tab(self, index):
        if index == 0:  # Pendulum
            O = self.Otrack[-1]
            w = self.wtrack[-1]
            x = self.xtrack[-1]
            v = self.vtrack[-1]
            F = self.Ftrack[-1]
            self.ipview.set_state(O, w, x, v, F)
        elif index == 1:  # Plots
            t = arange(0., 2.5, self.ip.dt)
            self.graph.set_multi_data([
                (t, self.Otrack), (t, self.wtrack),
                (t, self.xtrack), (t, self.vtrack),
                (t, zeros(t.shape))  # self.Ftrack)
            ])
        elif index == 2:  # Membership
            O = self.Otrack[-1]
            w = self.wtrack[-1]
            x = self.xtrack[-1]
            v = self.vtrack[-1]
            F = self.Ftrack[-1]
            self.feedback(O, w, x, v, F)

    def closeEvent(self, event):
        self.on_stop_button()
        self.app.exit(0)


if __name__ == "__main__":
    q = QApplication([])
    f = IPFrame(q, None)
    q.exec_()
