#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import wx
from db.sql_connector import DVH_SQL, echo_sql_db
from db.sql_settings import write_sql_connection_settings, validate_sql_connection
from paths import SQL_CNF_PATH, parse_settings_file


class CalculationsDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        wx.Dialog.__init__(self, None, title="Calculations")

        choices = ["PTV Distances", "PTV Overlap", "ROI Centroid", "ROI Spread", "ROI Cross-Section",
                   "OAR-PTV Centroid Distance", "Beam Complexities", "Plan Complexities", "All (except age)",
                   "Patient Ages"]
        self.combo_box_calculate = wx.ComboBox(self, wx.ID_ANY, choices=choices, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.checkbox = wx.CheckBox(self, wx.ID_ANY, "Only Calculate Missing Values")
        self.text_ctrl_condition = wx.TextCtrl(self, wx.ID_ANY, "")
        self.button_ok = wx.Button(self, wx.ID_OK, "Calculate")
        # TODO: Add functionality to OK button
        self.button_cancel = wx.Button(self, wx.ID_CANCEL, "Cancel")

        self.__set_properties()
        self.__do_layout()

        self.run()

    def __set_properties(self):
        self.checkbox.SetValue(1)

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_wrapper = wx.BoxSizer(wx.VERTICAL)
        sizer_wrapper_inner = wx.BoxSizer(wx.VERTICAL)
        sizer_ok_cancel = wx.BoxSizer(wx.HORIZONTAL)
        sizer_input = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, ""), wx.VERTICAL)
        sizer_condition = wx.BoxSizer(wx.VERTICAL)
        sizer_calc_and_check = wx.BoxSizer(wx.HORIZONTAL)
        sizer_calculate = wx.BoxSizer(wx.VERTICAL)
        label_calculate = wx.StaticText(self, wx.ID_ANY, "Calculate:")
        sizer_calculate.Add(label_calculate, 0, wx.BOTTOM, 5)
        sizer_calculate.Add(self.combo_box_calculate, 0, 0, 0)
        sizer_calc_and_check.Add(sizer_calculate, 0, wx.EXPAND, 0)
        sizer_calc_and_check.Add(self.checkbox, 0, wx.LEFT | wx.TOP, 20)
        sizer_input.Add(sizer_calc_and_check, 0, wx.BOTTOM | wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        label_condition = wx.StaticText(self, wx.ID_ANY, "Condition:")
        sizer_condition.Add(label_condition, 0, wx.BOTTOM, 5)
        sizer_condition.Add(self.text_ctrl_condition, 0, wx.EXPAND, 0)
        sizer_input.Add(sizer_condition, 0, wx.ALL | wx.EXPAND, 5)
        sizer_wrapper_inner.Add(sizer_input, 0, wx.ALL | wx.EXPAND, 5)
        sizer_ok_cancel.Add(self.button_ok, 0, wx.ALL, 5)
        sizer_ok_cancel.Add(self.button_cancel, 0, wx.ALL, 5)
        sizer_wrapper_inner.Add(sizer_ok_cancel, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        sizer_wrapper.Add(sizer_wrapper_inner, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_wrapper)
        sizer_wrapper.Fit(self)
        self.Layout()
        self.Center()

    def run(self):
        res = self.ShowModal()
        if res == wx.ID_OK:
            pass
        self.Destroy()


class BaseClass(wx.Dialog):
    def __init__(self, text_input_1_label, text_input_2_label, ok_button_label, title,
                 mrn=None, study_instance_uid=None, *args, **kw):
        wx.Dialog.__init__(self, None, title=title)

        self.mrn = mrn
        self.study_instance_uid = study_instance_uid

        self.text_input_1_label = text_input_1_label
        self.text_input_2_label = text_input_2_label

        self.combo_box_patient_identifier = wx.ComboBox(self, wx.ID_ANY, choices=["MRN", "Study Instance UID"],
                                                        style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.text_ctrl_1 = wx.TextCtrl(self, wx.ID_ANY, "")
        self.text_ctrl_2 = wx.TextCtrl(self, wx.ID_ANY, "")
        self.button_ok = wx.Button(self, wx.ID_OK, ok_button_label)
        self.button_cancel = wx.Button(self, wx.ID_CANCEL, "Cancel")

        self.__set_properties()
        self.__do_bind()
        self.__do_layout()

    def __set_properties(self):
        self.text_ctrl_1.SetMinSize((365, 22))
        self.on_identifier_change(None)

    def __do_layout(self):
        sizer_wrapper = wx.BoxSizer(wx.VERTICAL)
        sizer_ok_cancel = wx.BoxSizer(wx.HORIZONTAL)
        sizer_input = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, ""), wx.VERTICAL)
        sizer_new_value = wx.BoxSizer(wx.VERTICAL)
        sizer_value = wx.BoxSizer(wx.VERTICAL)
        sizer_patient_identifier = wx.BoxSizer(wx.HORIZONTAL)
        label_patient_identifier = wx.StaticText(self, wx.ID_ANY, "Patient Identifier:")
        sizer_patient_identifier.Add(label_patient_identifier, 0, wx.ALL, 5)
        sizer_patient_identifier.Add(self.combo_box_patient_identifier, 0, wx.TOP, 2)
        sizer_input.Add(sizer_patient_identifier, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        label_text_input_1 = wx.StaticText(self, wx.ID_ANY, self.text_input_1_label)
        sizer_value.Add(label_text_input_1, 0, wx.EXPAND | wx.ALL, 5)
        sizer_value.Add(self.text_ctrl_1, 0, wx.BOTTOM | wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        sizer_input.Add(sizer_value, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        label_text_input_2 = wx.StaticText(self, wx.ID_ANY, self.text_input_2_label)
        sizer_new_value.Add(label_text_input_2, 0, wx.EXPAND | wx.ALL, 5)
        sizer_new_value.Add(self.text_ctrl_2, 0, wx.BOTTOM | wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        sizer_input.Add(sizer_new_value, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        sizer_wrapper.Add(sizer_input, 0, wx.LEFT | wx.RIGHT | wx.TOP, 10)
        sizer_ok_cancel.Add(self.button_ok, 0, wx.ALL, 5)
        sizer_ok_cancel.Add(self.button_cancel, 0, wx.ALL, 5)
        sizer_wrapper.Add(sizer_ok_cancel, 0, wx.ALIGN_RIGHT | wx.BOTTOM | wx.RIGHT, 10)
        self.SetSizer(sizer_wrapper)
        sizer_wrapper.Fit(self)
        self.Layout()
        self.Center()

    def __do_bind(self):
        self.Bind(wx.EVT_COMBOBOX, self.on_identifier_change, id=self.combo_box_patient_identifier.GetId())

    def run(self):
        res = self.ShowModal()
        if res == wx.ID_OK:
            self.action()
        self.Destroy()

    def action(self):
        pass

    def on_identifier_change(self, evt):
        value = {'Study Instance UID': self.study_instance_uid,
                 'MRN': self.mrn}[self.combo_box_patient_identifier.GetValue()]
        if value is not None:
            self.text_ctrl_1.SetValue(value)
            wx.CallAfter(self.text_ctrl_2.SetFocus)

    @property
    def selected_id_type(self):
        return self.combo_box_patient_identifier.GetValue().lower().replace(' ', '_')


class ChangePatientIdentifierDialog(BaseClass):
    def __init__(self, mrn=None, study_instance_uid=None, *args, **kw):
        BaseClass.__init__(self, 'Value:', 'New Value:', 'Change', "Change Patient Identifier",
                           mrn=mrn, study_instance_uid=study_instance_uid)

        self.run()

    def action(self):
        old_id = self.text_ctrl_1.GetValue()
        new_id = self.text_ctrl_2.GetValue()

        with DVH_SQL() as cnx:
            validation_func = [cnx.is_uid_imported, cnx.is_mrn_imported][self.selected_id_type == 'mrn']
            change_func = [cnx.change_uid, cnx.change_mrn][self.selected_id_type == 'mrn']

        if validation_func(old_id):
            if self.selected_id_type == 'study_instance_uid' and validation_func(new_id):
                wx.MessageBox('This Study Instance UID is already in use.',
                              '%s Error' % self.combo_box_patient_identifier.GetValue(),
                              wx.OK | wx.ICON_WARNING)
            else:
                change_func(old_id, new_id)
        else:
            wx.MessageBox('No studies found with this %s.' % self.combo_box_patient_identifier.GetValue(),
                          '%s Error' % self.combo_box_patient_identifier.GetValue(),
                          wx.OK | wx.ICON_WARNING)


class DeletePatientDialog(BaseClass):
    def __init__(self, mrn=None, study_instance_uid=None, *args, **kw):
        BaseClass.__init__(self, 'Delete:', 'Type "delete" to authorize:', 'Delete', "Delete Patient",
                           mrn=mrn, study_instance_uid=study_instance_uid)

        self.run()

    def action(self):
        if self.text_ctrl_2.GetValue() == 'delete':
            column = self.selected_id_type.lower().replace(' ', '_')
            value = self.text_ctrl_1.GetValue()
            with DVH_SQL() as cnx:
                cnx.delete_rows("%s = '%s'" % (column, value))


class EditDatabaseDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        wx.Dialog.__init__(self, None, title="Edit Database Values")

        self.combo_box_table = wx.ComboBox(self, wx.ID_ANY, choices=self.get_tables(),
                                           style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.combo_box_column = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.text_ctrl_value = wx.TextCtrl(self, wx.ID_ANY, "")
        self.text_ctrl_condition = wx.TextCtrl(self, wx.ID_ANY, "")
        self.button_ok = wx.Button(self, wx.ID_OK, "Update")
        self.button_cancel = wx.Button(self, wx.ID_CANCEL, "Cancel")

        self.Bind(wx.EVT_COMBOBOX, self.OnTable, id=self.combo_box_table.GetId())

        self.__set_properties()
        self.__do_layout()

        self.update_columns()

        self.run()

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        # self.SetTitle("frame")
        # end wxGlade
        pass

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_wrapper = wx.BoxSizer(wx.VERTICAL)
        sizer_wrapper_inner = wx.BoxSizer(wx.VERTICAL)
        sizer_ok_cancel = wx.BoxSizer(wx.HORIZONTAL)
        sizer_input = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, ""), wx.VERTICAL)
        sizer_condition = wx.BoxSizer(wx.VERTICAL)
        sizer_table_column_value = wx.BoxSizer(wx.HORIZONTAL)
        sizer_value = wx.BoxSizer(wx.VERTICAL)
        sizer_column = wx.BoxSizer(wx.VERTICAL)
        sizer_table = wx.BoxSizer(wx.VERTICAL)
        label_table = wx.StaticText(self, wx.ID_ANY, "Table:")
        sizer_table.Add(label_table, 0, 0, 0)
        sizer_table.Add(self.combo_box_table, 0, wx.EXPAND, 0)
        sizer_table_column_value.Add(sizer_table, 0, wx.ALL | wx.EXPAND, 5)
        label_column = wx.StaticText(self, wx.ID_ANY, "Column:")
        sizer_column.Add(label_column, 0, 0, 0)
        sizer_column.Add(self.combo_box_column, 0, 0, 0)
        sizer_table_column_value.Add(sizer_column, 0, wx.ALL | wx.EXPAND, 5)
        label_value = wx.StaticText(self, wx.ID_ANY, "Value:")
        sizer_value.Add(label_value, 0, 0, 0)
        sizer_value.Add(self.text_ctrl_value, 0, wx.EXPAND, 0)
        sizer_table_column_value.Add(sizer_value, 1, wx.ALL | wx.EXPAND, 5)
        sizer_input.Add(sizer_table_column_value, 1, wx.EXPAND, 0)
        label_condition = wx.StaticText(self, wx.ID_ANY, "Condition:")
        sizer_condition.Add(label_condition, 0, wx.BOTTOM | wx.RIGHT | wx.TOP, 5)
        sizer_condition.Add(self.text_ctrl_condition, 0, wx.EXPAND, 0)
        sizer_input.Add(sizer_condition, 1, wx.BOTTOM | wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        sizer_wrapper_inner.Add(sizer_input, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        sizer_ok_cancel.Add(self.button_ok, 0, wx.ALL, 5)
        sizer_ok_cancel.Add(self.button_cancel, 0, wx.ALL, 5)
        sizer_wrapper_inner.Add(sizer_ok_cancel, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        sizer_wrapper.Add(sizer_wrapper_inner, 0, wx.ALL | wx.EXPAND, 0)
        self.SetSizer(sizer_wrapper)
        sizer_wrapper.Fit(self)
        self.Layout()
        self.Center()

    @staticmethod
    def get_tables():
        with DVH_SQL() as cnx:
            tables = cnx.tables
        return tables

    def update_columns(self):
        table = self.combo_box_table.GetValue()
        with DVH_SQL() as cnx:
            columns = cnx.get_column_names(table)
        self.combo_box_column.SetItems(columns)
        if self.combo_box_column.GetValue() not in columns:
            self.combo_box_column.SetValue(columns[0])

    def OnTable(self, evt):
        self.update_columns()

    def run(self):
        res = self.ShowModal()
        if res == wx.ID_OK:
            pass
        self.Destroy()


class ReimportDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        wx.Dialog.__init__(self, None, title="Reimport from DICOM")

        self.text_ctrl_mrn = wx.TextCtrl(self, wx.ID_ANY, "")
        self.radio_box_delete_from_db = wx.RadioBox(self, wx.ID_ANY, "Current Data",
                                                    choices=["Delete from DB", "Keep in DB"],
                                                    majorDimension=2, style=wx.RA_SPECIFY_ROWS)
        self.combo_box_study_date = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.combo_box_uid = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.button_reimport = wx.Button(self, wx.ID_OK, "Reimport")
        self.button_cancel = wx.Button(self, wx.ID_CANCEL, "Cancel")

        self.__set_properties()
        self.__do_layout()

        self.run()

    def __set_properties(self):
        self.radio_box_delete_from_db.SetSelection(0)
        self.combo_box_study_date.SetMinSize((200, 25))

    def __do_layout(self):
        sizer_wrapper = wx.BoxSizer(wx.VERTICAL)
        sizer_ok_cancel = wx.BoxSizer(wx.HORIZONTAL)
        sizer_input = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, ""), wx.VERTICAL)
        sizer_input_date_uid = wx.BoxSizer(wx.HORIZONTAL)
        sizer_uid = wx.BoxSizer(wx.VERTICAL)
        sizer_input_date = wx.BoxSizer(wx.VERTICAL)
        sizer_input_mrn_db = wx.BoxSizer(wx.HORIZONTAL)
        sizer_mrn = wx.BoxSizer(wx.VERTICAL)
        label_mrn = wx.StaticText(self, wx.ID_ANY, "MRN:")
        sizer_mrn.Add(label_mrn, 0, wx.BOTTOM, 5)
        sizer_mrn.Add(self.text_ctrl_mrn, 0, wx.EXPAND | wx.RIGHT, 40)
        sizer_input_mrn_db.Add(sizer_mrn, 1, wx.TOP, 12)
        sizer_input_mrn_db.Add(self.radio_box_delete_from_db, 0, wx.ALL, 5)
        sizer_input.Add(sizer_input_mrn_db, 0, wx.EXPAND | wx.LEFT, 5)
        label_date = wx.StaticText(self, wx.ID_ANY, "Sim Study Date:")
        sizer_input_date.Add(label_date, 0, wx.BOTTOM, 5)
        sizer_input_date.Add(self.combo_box_study_date, 0, 0, 0)
        sizer_input_date_uid.Add(sizer_input_date, 0, wx.ALL | wx.EXPAND, 5)
        label_uid = wx.StaticText(self, wx.ID_ANY, "Study Instance UID:")
        sizer_uid.Add(label_uid, 0, wx.BOTTOM, 5)
        sizer_uid.Add(self.combo_box_uid, 0, wx.EXPAND, 0)
        sizer_input_date_uid.Add(sizer_uid, 1, wx.ALL | wx.EXPAND, 5)
        sizer_input.Add(sizer_input_date_uid, 0, wx.EXPAND, 0)
        sizer_wrapper.Add(sizer_input, 0, wx.ALL | wx.EXPAND, 5)
        sizer_ok_cancel.Add(self.button_reimport, 0, wx.ALL, 5)
        sizer_ok_cancel.Add(self.button_cancel, 0, wx.ALL, 5)
        sizer_wrapper.Add(sizer_ok_cancel, 0, wx.ALIGN_RIGHT | wx.BOTTOM | wx.RIGHT, 5)
        self.SetSizer(sizer_wrapper)
        sizer_wrapper.SetMinSize((700, 190))
        sizer_wrapper.Fit(self)
        self.Layout()
        self.Center()

    def run(self):
        res = self.ShowModal()
        if res == wx.ID_OK:
            pass
        self.Destroy()


class SQLSettingsDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        wx.Dialog.__init__(self, None, title="Database Connection Settings")

        self.keys = ['host', 'port', 'dbname', 'user', 'password']

        self.input = {key: wx.TextCtrl(self, wx.ID_ANY, "") for key in self.keys if key != 'password'}
        self.input['password'] = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_PASSWORD)
        self.button = {'ok': wx.Button(self, wx.ID_OK, "OK"),
                       'cancel': wx.Button(self, wx.ID_CANCEL, "Cancel"),
                       'echo': wx.Button(self, wx.ID_ANY, "Echo")}

        self.Bind(wx.EVT_BUTTON, self.button_echo, id=self.button['echo'].GetId())

        self.__set_properties()
        self.__do_layout()
        self.Center()

        self.load_sql_settings()

    def __set_properties(self):
        self.SetTitle("SQL Connection Settings")

    def __do_layout(self):
        sizer_frame = wx.BoxSizer(wx.VERTICAL)
        sizer_echo = wx.BoxSizer(wx.HORIZONTAL)
        sizer_buttons = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer = wx.GridSizer(5, 2, 5, 10)

        label_titles = ['Host:', 'Port:', 'Database Name:', 'User Name:', 'Password:']
        label = {key: wx.StaticText(self, wx.ID_ANY, label_titles[i]) for i, key in enumerate(self.keys)}

        for key in self.keys:
            grid_sizer.Add(label[key], 0, wx.ALL, 0)
            grid_sizer.Add(self.input[key], 0, wx.ALL | wx.EXPAND, 0)

        sizer_frame.Add(grid_sizer, 0, wx.ALL, 10)
        sizer_buttons.Add(self.button['ok'], 1, wx.ALL | wx.EXPAND, 5)
        sizer_buttons.Add(self.button['cancel'], 1, wx.ALL | wx.EXPAND, 5)
        sizer_echo.Add(self.button['echo'], 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 5)
        sizer_frame.Add(sizer_echo, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 5)
        sizer_frame.Add(sizer_buttons, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(sizer_frame)
        self.Fit()
        self.Layout()

    def load_sql_settings(self):
        config = parse_settings_file(SQL_CNF_PATH)

        for input_type in self.keys:
            if input_type in config:
                self.input[input_type].SetValue(config[input_type])

    def button_echo(self, evt):
        if self.valid_sql_settings:
            wx.MessageBox('Success!', 'Echo SQL Database', wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox('Invalid credentials!', 'Echo SQL Database', wx.OK | wx.ICON_WARNING)

    @property
    def valid_sql_settings(self):
        config = {key: self.input[key].GetValue() for key in self.keys if self.input[key].GetValue()}
        return echo_sql_db(config)


def run_sql_settings_dlg():
    dlg = SQLSettingsDialog()
    res = dlg.ShowModal()
    if res == wx.ID_OK:
        new_config = {key: dlg.input[key].GetValue() for key in dlg.keys if dlg.input[key].GetValue()}
        write_sql_connection_settings(new_config)
        if not validate_sql_connection(new_config):
            dlg = wx.MessageDialog(dlg, 'Connection to database could not be established.', 'ERROR!', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
    dlg.Destroy()

    return res
