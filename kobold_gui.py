#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.5 on Mon May 14 00:59:34 2007 from /home/synack/hoefelmeyer_kme/Gabelstaplersystem/sensor_simulator/kobold_gui.wxg

#Copyright (c) 2007 Haiko Schol (http://www.haikoschol.com/)
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

from kobold_controller import *
import wx

class ConfigDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: ConfigDialog.__init__
        kwds["style"] = wx.CAPTION|wx.CLOSE_BOX
        wx.Dialog.__init__(self, *args, **kwds)
        self.sizer_12_staticbox = wx.StaticBox(self, -1, "Measuring Range")
        self.label_11 = wx.StaticText(self, -1, "Serial Port")
        self.serial_port_combo_box = wx.ComboBox(self, -1, choices=[], style=wx.CB_DROPDOWN|wx.CB_DROPDOWN|wx.CB_SORT)
        self.label_12 = wx.StaticText(self, -1, "Device Identifier")
        self.device_id_text_ctrl = wx.TextCtrl(self, -1, "")
        self.label_13 = wx.StaticText(self, -1, "Temperature")
        self.temperature_text_ctrl = wx.TextCtrl(self, -1, "")
        self.label_9 = wx.StaticText(self, -1, "Begin")
        self.range_begin_spin_ctrl = wx.SpinCtrl(self, -1, "0", min=0, max=999, style=wx.TE_READONLY)
        self.label_10 = wx.StaticText(self, -1, "End")
        self.range_end_spin_ctrl = wx.SpinCtrl(self, -1, "1000", min=0, max=1000, style=wx.TE_READONLY)
        self.ok_button = wx.Button(self, wx.ID_OK, "OK")
        self.ok_button.SetDefault()
        self.cancel_button = wx.Button(self, wx.ID_CANCEL, "Cancel")

        self.__set_properties()
        self.__do_layout()

        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: ConfigDialog.__set_properties
        self.SetTitle("Configuration")
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: ConfigDialog.__do_layout
        sizer_9 = wx.BoxSizer(wx.VERTICAL)
        sizer_15 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_12 = wx.StaticBoxSizer(self.sizer_12_staticbox, wx.HORIZONTAL)
        sizer_14 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_13 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_1 = wx.GridSizer(3, 2, 5, 5)
        grid_sizer_1.Add(self.label_11, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.serial_port_combo_box, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.label_12, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.device_id_text_ctrl, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.label_13, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.temperature_text_ctrl, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        sizer_9.Add(grid_sizer_1, 1, wx.EXPAND, 0)
        sizer_13.Add(self.label_9, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        sizer_13.Add(self.range_begin_spin_ctrl, 0, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 5)
        sizer_12.Add(sizer_13, 1, wx.LEFT|wx.TOP|wx.BOTTOM|wx.EXPAND, 5)
        sizer_14.Add(self.label_10, 0, wx.LEFT|wx.RIGHT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 5)
        sizer_14.Add(self.range_end_spin_ctrl, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        sizer_12.Add(sizer_14, 1, wx.TOP|wx.BOTTOM|wx.EXPAND|wx.ALIGN_RIGHT, 5)
        sizer_9.Add(sizer_12, 0, wx.ALL|wx.EXPAND, 5)
        sizer_15.Add(self.ok_button, 0, wx.TOP|wx.BOTTOM|wx.ALIGN_RIGHT|wx.ADJUST_MINSIZE, 5)
        sizer_15.Add(self.cancel_button, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ADJUST_MINSIZE, 5)
        sizer_9.Add(sizer_15, 0, wx.ALIGN_RIGHT, 0)
        self.SetSizer(sizer_9)
        sizer_9.Fit(self)
        self.Layout()
        # end wxGlade
# end of class ConfigDialog


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.ICONIZE|wx.CAPTION|wx.MINIMIZE|wx.CLOSE_BOX|wx.MINIMIZE_BOX
        self.controller = kwds['controller']
        kwds.pop('controller')
        wx.Frame.__init__(self, *args, **kwds)
        self.panel_1 = wx.Panel(self, -1)
        self.sizer_4_staticbox = wx.StaticBox(self.panel_1, -1, "Data Source Parameters")
        self.sizer_7_staticbox = wx.StaticBox(self, -1, "Poll Mode Reply Delay")
        self.sizer_5_staticbox = wx.StaticBox(self, -1, "Sensor Parameters")
        self.sizer_3_staticbox = wx.StaticBox(self.panel_1, -1, "Data Log File")
        
        # Menu Bar
        self.frame_1_menubar = wx.MenuBar()
        self.SetMenuBar(self.frame_1_menubar)
        wxglade_tmp_menu = wx.Menu()
        self.settings_menu_item = wxglade_tmp_menu.Append(wx.NewId(), "&Settings", "", wx.ITEM_NORMAL)
        self.quit_menu_item = wxglade_tmp_menu.Append(wx.NewId(), "&Quit", "", wx.ITEM_NORMAL)
        self.frame_1_menubar.Append(wxglade_tmp_menu, "&File")
        # Menu Bar end
        self.statusbar = self.CreateStatusBar(1, 0)
        self.load_file_button = wx.Button(self.panel_1, -1, "Load File")
        self.toggle_replay_button = wx.ToggleButton(self.panel_1, -1, "Start Replay")
        self.reset_button = wx.Button(self.panel_1, -1, "Reset Replay")
        self.baseline_text_ctrl = wx.TextCtrl(self.panel_1, -1, str(self.controller.baseline), style=wx.TE_PROCESS_ENTER)
        self.set_baseline_button = wx.Button(self.panel_1, -1, "Set Baseline")
        self.variation_text_ctrl = wx.TextCtrl(self.panel_1, -1, str(self.controller.variation), style=wx.TE_PROCESS_ENTER)
        self.set_variation_button = wx.Button(self.panel_1, -1, "Set Variation")
        self.mode_radio_box = wx.RadioBox(self, -1, "Mode", choices=["Poll Mode", "Cyclic Output Pressure", "Cyclic Ouput Pressure And Temperature"], majorDimension=3, style=wx.RA_SPECIFY_ROWS)
        self.mode_radio_box.SetSelection(self.controller.mode-1)
        self.reply_delay_slider = wx.Slider(self, -1, self.controller.poll_mode_reply_delay, 0, 15, style=wx.SL_HORIZONTAL|wx.SL_LABELS)
        self.label_4 = wx.StaticText(self, -1, "Cyclic Output Mode Interval")
        self.interval_spin_ctrl = wx.SpinCtrl(self, -1, str(self.controller.cyclic_output_interval), min=1, max=65535, style=wx.TE_PROCESS_ENTER)

        self.__set_properties()
        self.__do_layout()

        self.controller.register(self.notification_handler)
        self.set_status_on_interval_and_delay_widget()

        self.Bind(wx.EVT_MENU, self.show_config_dialog, self.settings_menu_item)
        self.Bind(wx.EVT_MENU, self.quit_app, self.quit_menu_item)
        self.Bind(wx.EVT_BUTTON, self.load_file, self.load_file_button)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.toggle_replay, self.toggle_replay_button)
        self.Bind(wx.EVT_BUTTON, self.reset_replay, self.reset_button)
        self.Bind(wx.EVT_TEXT_ENTER, self.baseline_enter, self.baseline_text_ctrl)
        self.Bind(wx.EVT_BUTTON, self.set_baseline, self.set_baseline_button)
        self.Bind(wx.EVT_TEXT_ENTER, self.variation_enter, self.variation_text_ctrl)
        self.Bind(wx.EVT_BUTTON, self.set_variation, self.set_variation_button)
        self.Bind(wx.EVT_RADIOBOX, self.set_mode, self.mode_radio_box)
        self.Bind(wx.EVT_COMMAND_SCROLL_ENDSCROLL, self.set_reply_delay, self.reply_delay_slider)
        self.Bind(wx.EVT_SPINCTRL, self.set_output_interval, self.interval_spin_ctrl)
        self.Bind(wx.EVT_CLOSE, self.quit_app)

        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("Kobold SEM 3 Sensor Simulator")
        self.statusbar.SetStatusWidths([-1])
        # statusbar fields
        statusbar_fields = [""]
        for i in range(len(statusbar_fields)):
            self.statusbar.SetStatusText(statusbar_fields[i], i)
        self.toggle_replay_button.Enable(False)
        self.reset_button.Enable(False)
        self.mode_radio_box.SetSelection(0)
        self.reply_delay_slider.SetMinSize((345, 38))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_5 = wx.StaticBoxSizer(self.sizer_5_staticbox, wx.VERTICAL)
        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7 = wx.StaticBoxSizer(self.sizer_7_staticbox, wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.StaticBoxSizer(self.sizer_4_staticbox, wx.HORIZONTAL)
        sizer_3 = wx.StaticBoxSizer(self.sizer_3_staticbox, wx.HORIZONTAL)
        sizer_3.Add(self.load_file_button, 0, wx.ALL|wx.ADJUST_MINSIZE, 5)
        sizer_3.Add(self.toggle_replay_button, 0, wx.RIGHT|wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 5)
        sizer_3.Add(self.reset_button, 0, wx.RIGHT|wx.TOP|wx.BOTTOM|wx.ADJUST_MINSIZE, 5)
        sizer_2.Add(sizer_3, 0, wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_HORIZONTAL, 5)
        sizer_4.Add(self.baseline_text_ctrl, 0, wx.LEFT|wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 5)
        sizer_4.Add(self.set_baseline_button, 0, wx.RIGHT|wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 5)
        sizer_4.Add(self.variation_text_ctrl, 0, wx.LEFT|wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 5)
        sizer_4.Add(self.set_variation_button, 0, wx.RIGHT|wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 5)
        sizer_2.Add(sizer_4, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.panel_1.SetSizer(sizer_2)
        sizer_1.Add(self.panel_1, 0, wx.ADJUST_MINSIZE, 0)
        sizer_5.Add(self.mode_radio_box, 0, wx.ALL|wx.EXPAND|wx.ADJUST_MINSIZE, 5)
        sizer_7.Add(self.reply_delay_slider, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        sizer_5.Add(sizer_7, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_8.Add(self.label_4, 0, wx.ALL|wx.ADJUST_MINSIZE, 5)
        sizer_8.Add(self.interval_spin_ctrl, 0, wx.BOTTOM|wx.ADJUST_MINSIZE, 5)
        sizer_5.Add(sizer_8, 0, wx.EXPAND, 0)
        sizer_1.Add(sizer_5, 0, wx.ALL, 5)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade

    def notification_handler(self, source, arg):
        try:
            getattr(self, 'handle_' + arg[0] + '_update')(arg[1])
        except AttributeError:
            pass

    def handle_mode_update(self, mode):
        if self.mode_radio_box.GetSelection() != mode-1:
            self.set_status_on_interval_and_delay_widget()

    def handle_poll_mode_reply_delay_update(self, delay):
        if self.reply_delay_slider.GetValue() != delay:
            self.reply_delay_slider.SetValue(delay)
            if self.reply_delay_slider.Disabled():
                self.reply_delay_slider.Enable(True)
                self.reply_delay_slider.Disable()

    def handle_cyclic_output_interval_update(self, interval):
        if self.interval_spin_ctrl.GetValue() != interval:
            self.interval_spin_ctrl.SetValue(interval)
            if self.interval_spin_ctrl.Disabled():
                self.interval_spin_ctrl.Enable(True)
                self.interval_spin_ctrl.Disable()

    def handle_baseline_update(self, baseline):
        if float(self.baseline_text_ctrl.GetValue()) != baseline:
            self.baseline_text_ctrl.SetValue(str(baseline))

    def handle_variation_update(self, variation):
        if float(self.variation_text_ctrl.GetValue()) != variation:
            self.variation_text_ctrl.SetValue(str(variation))

    def show_configuration_dialog(self):
        dlg = ConfigDialog(None)
        dlg.serial_port_combo_box.Clear()
        if self.controller.serial_port:
            dlg.serial_port_combo_box.Append(self.controller.serial_port)
        dlg.serial_port_combo_box.AppendItems(self.controller.get_serial_port_default_names())
        dlg.device_id_text_ctrl.SetValue(self.controller.device_identifier)
        dlg.temperature_text_ctrl.SetValue(str(self.controller.temperature))
        dlg.range_begin_spin_ctrl.SetValue(self.controller.measuring_range_begin)
        dlg.range_end_spin_ctrl.SetValue(self.controller.measuring_range_end)
        done = False

        while not done:
            if dlg.ShowModal() == wx.ID_OK:
                try:
                    self.controller.serial_port = dlg.serial_port_combo_box.GetValue()
                    self.controller.device_identifier = dlg.device_id_text_ctrl.GetValue()
                    self.controller.temperature = dlg.temperature_text_ctrl.GetValue()
                    self.controller.measuring_range_begin = dlg.range_begin_spin_ctrl.GetValue()
                    self.controller.measuring_range_end = dlg.range_end_spin_ctrl.GetValue()
                    self.controller.save_configuration()
                    done = True
                except Exception, err:
                    wx.MessageBox(str(err), 'An error occured.', style=wx.ICON_ERROR|wx.OK)
            else:
                done = True
        dlg.Destroy()

    def set_status_on_interval_and_delay_widget(self):
        self.mode_radio_box.SetSelection(self.controller.sensor.mode-1)

        if self.controller.mode == KoboldSimulator.POLL_MODE:
            self.reply_delay_slider.Enable(True)
            self.interval_spin_ctrl.Disable()
        else:
            self.reply_delay_slider.Disable()
            self.interval_spin_ctrl.Enable(True)

    def load_file(self, event): # wxGlade: MyFrame.<event_handler>
        dlg = wx.FileDialog(self, 'Choose a File with Recorded Data', style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            try:
                self.controller.load_data_log_file(dlg.GetPath())
            except DataLogFileFormatError, ex:
                wx.MessageBox(str(ex), caption='Could not read file', style=wx.OK|wx.ICON_ERROR)
                return
        self.toggle_replay_button.Enable(True)
        self.reset_button.Enable(True)

    def toggle_replay(self, event): # wxGlade: MyFrame.<event_handler>
        self.reset_button.Enable(True)
        if self.toggle_replay_button.GetValue():
            self.controller.start_replay()
        else:
            self.controller.stop_replay()

    def reset_replay(self, event): # wxGlade: MyFrame.<event_handler>
        self.controller.reset_replay()

    def baseline_enter(self, event): # wxGlade: MyFrame.<event_handler>
        self.set_baseline(event)

    def set_baseline(self, event): # wxGlade: MyFrame.<event_handler>
        try:
            self.controller.baseline = float(self.baseline_text_ctrl.GetValue())
        except ValueError, err:
            wx.MessageBox(str(err), 'An error occurred', style=wx.OK|wx.ICON_ERROR)
            self.baseline_text_ctrl.SetValue(str(self.controller.baseline))

    def variation_enter(self, event): # wxGlade: MyFrame.<event_handler>
        self.set_variation(event)

    def set_variation(self, event): # wxGlade: MyFrame.<event_handler>
        try:
            self.controller.variation = float(self.variation_text_ctrl.GetValue())
        except ValueError, err:
            wx.MessageBox(str(err), 'An error occurred', style=wx.OK|wx.ICON_ERROR)
            self.variation_text_ctrl.SetValue(str(self.controller.variation))

    def set_mode(self, event): # wxGlade: MyFrame.<event_handler>
        self.controller.mode = self.mode_radio_box.GetSelection()+1
        self.set_status_on_interval_and_delay_widget()

    def set_reply_delay(self, event): # wxGlade: MyFrame.<event_handler>
        self.controller.poll_mode_reply_delay = self.reply_delay_slider.GetValue()

    def set_output_interval(self, event): # wxGlade: MyFrame.<event_handler>
        try:
            self.controller.cyclic_output_interval = self.interval_spin_ctrl.GetValue()
        except ValueError, err:
            wx.MessageBox(str(err), 'An error occurred', style=wx.OK|wx.ICON_ERROR)

    def show_config_dialog(self, event): # wxGlade: MyFrame.<event_handler>
        self.show_configuration_dialog()

    def quit_app(self, event): # wxGlade: MyFrame.<event_handler>
        self.controller.save_configuration()
        self.controller.close()
        self.Destroy()

# end of class MyFrame


class MyApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        frame_1 = MyFrame(None, -1, "", controller=KoboldController())
        self.SetTopWindow(frame_1)
        frame_1.Show()
        return 1

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
