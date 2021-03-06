#! /usr/bin/python

"""
Main module to aid in learning how to subnet quickly.

SHORTCUT KEYS:
    * CTRL + N     -> Generate a new network to guess.
    * CTRL + R     -> Reveal the answers.
    * RETURN/ENTER -> Check answers (only if focus is on any of the
                                     guess entry boxes).
    * ALT + A      -> Toggle Class A CheckButton.
    * ALT + B      -> Toggle Class B CheckButton.
    * ALT + C      -> Toggle Class C CheckButton.
    * ALT + T      -> Toggle Timer On/Off

AUTHOR:    T.WINN
CREATED:   16 April 2016
MODIFIED:  20 April 2016
VERSION:   1.2
"""

# STDLIB IMPORTS
import random
import gtk

# LOCAL IMPORTS
from NetworkClass import class_a, class_b, class_c
from AnswerClass import Answer
from constants import (UPPER_CIDR_VALUE, LOWER_OCTET_VALUE, UPPER_OCTET_VALUE)


class SubnetTester(gtk.Window):
    """
    SubnetTester class which combines the GUI with the logic.
    """

    def __init__(self):
        """
        Initialise an instance of SubnetTester.
        """
        super(SubnetTester, self).__init__()
        self.set_title(title="Subnet Tester")
        self.connect("delete-event", gtk.main_quit)

        self._content_area = gtk.VBox()
        self.add(self._content_area)

        self._generate_file_menu()

        self._generate_class_option_frame()

        self._content_area.pack_start(child=gtk.HSeparator(), expand=False, fill=False, padding=5)

        # self._generate_timing_container()

        self._content_area.pack_start(child=gtk.HSeparator(), expand=False, fill=False, padding=5)
        self._generate_network_to_guess_container()
        self._generate_guess_container()

        self.show_all()

        self.class_check_list = ["class_c"]

        self.answer = None

        self._generate_network_to_guess()

    def _parse_settings(self):
        """
        Parse the settings.ini file.
        """

    ###########################################################################
    #                               UI GENERATION                             #
    ###########################################################################
    def _generate_file_menu(self):
        """
        Generate the file menu.
        """
        menu_bar = gtk.MenuBar()

        menu_acc = gtk.AccelGroup()
        self.add_accel_group(menu_acc)

        ###############################################################
        #                             FILE                            #
        ###############################################################
        file_menu = gtk.Menu()
        file_sub = gtk.MenuItem("_File")
        file_sub.set_submenu(file_menu)

        exit_item = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        key, modifier = gtk.accelerator_parse("<alt>F4")
        exit_item.add_accelerator(accel_signal="activate", accel_group=menu_acc, accel_key=key,
                                  accel_mods=modifier, accel_flags=gtk.ACCEL_VISIBLE)
        exit_item.connect("activate", gtk.main_quit)
        file_menu.append(exit_item)

        menu_bar.append(file_sub)

        ###############################################################
        #                           SETTINGS                          #
        ###############################################################
        settings_menu = gtk.Menu()
        settings_sub = gtk.MenuItem("_Settings")
        settings_sub.set_submenu(settings_menu)

        settings_item = gtk.MenuItem("Settings")
        key, modifier = gtk.accelerator_parse("<alt>p")
        settings_item.add_accelerator(accel_signal="activate", accel_group=menu_acc, accel_key=key,
                                      accel_mods=modifier, accel_flags=gtk.ACCEL_VISIBLE)
        # settings_item.connect("activate", NotImplementedError)
        settings_menu.append(settings_item)

        # ----------------------------------------------------------- #

        separator = gtk.SeparatorMenuItem()
        settings_menu.append(separator)

        # ----------------------------------------------------------- #

        timer_enable_item = gtk.CheckMenuItem("Timer")
        # timer_enable_item.set_active(True)
        key, modifier = gtk.accelerator_parse("<alt>t")
        timer_enable_item.add_accelerator(accel_signal="activate", accel_group=menu_acc,
                                          accel_key=key, accel_mods=modifier,
                                          accel_flags=gtk.ACCEL_VISIBLE)
        timer_enable_item.connect("toggled", self._timer_enabled_checkbutton_toggled)
        settings_menu.append(timer_enable_item)

        menu_bar.append(settings_sub)

        self._content_area.pack_start(child=menu_bar, fill=False, expand=False, padding=0)

    def _generate_class_option_frame(self):
        """
        Generate the frame to select the class(es) to generate subnets
        for.
        """
        class_frame = gtk.Frame(label=" Class Select")
        class_frame.set_shadow_type(type=gtk.SHADOW_NONE)
        class_box = gtk.HBox()
        class_frame.add(class_box)

        class_accel_group = gtk.AccelGroup()
        self.add_accel_group(class_accel_group)

        # ----------------------------------------------------------- #
        class_a_box = gtk.HBox()

        class_a_label = gtk.Label()
        class_a_label.set_text_with_mnemonic("Class _A:")
        class_a_box.pack_start(child=class_a_label, expand=False, fill=False, padding=0)

        self.class_a_check = gtk.CheckButton()
        self.class_a_check.connect("toggled", self._class_checkbutton_toggled, "class_a")

        # assign the label mnemonic to the class_a_check
        class_a_label.set_mnemonic_widget(self.class_a_check)
        self.class_a_check.add_accelerator(accel_signal="clicked", accel_group=class_accel_group,
                                           accel_key=gtk.gdk.keyval_from_name('a'),
                                           accel_mods=gtk.gdk.MOD1_MASK, accel_flags=0)

        class_a_box.pack_start(child=self.class_a_check, expand=False, fill=False, padding=0)

        class_box.pack_start(child=class_a_box, expand=False, fill=False, padding=5)

        # ----------------------------------------------------------- #
        class_b_box = gtk.HBox()

        class_b_label = gtk.Label()
        class_b_label.set_text_with_mnemonic("Class _B:")
        class_b_box.pack_start(child=class_b_label, expand=False, fill=False, padding=0)

        self.class_b_check = gtk.CheckButton()
        self.class_b_check.connect("toggled", self._class_checkbutton_toggled, "class_b")

        # assign the label mnemonic to the class_b_check
        class_b_label.set_mnemonic_widget(self.class_b_check)
        self.class_b_check.add_accelerator(accel_signal="clicked", accel_group=class_accel_group,
                                           accel_key=gtk.gdk.keyval_from_name('b'),
                                           accel_mods=gtk.gdk.MOD1_MASK, accel_flags=0)

        class_b_box.pack_start(child=self.class_b_check, expand=False, fill=False, padding=0)

        class_box.pack_start(child=class_b_box, expand=False, fill=False, padding=5)

        # ----------------------------------------------------------- #
        class_c_box = gtk.HBox()

        class_c_label = gtk.Label()
        class_c_label.set_text_with_mnemonic("Class _C:")
        class_c_box.pack_start(child=class_c_label, expand=False, fill=False, padding=0)

        self.class_c_check = gtk.CheckButton()
        # set the Class C check button to active by default.
        self.class_c_check.set_active(True)
        self.class_c_check.connect("toggled", self._class_checkbutton_toggled, "class_c")

        # assign the label mnemonic to the class_c_check
        class_c_label.set_mnemonic_widget(self.class_c_check)
        self.class_c_check.add_accelerator(accel_signal="clicked", accel_group=class_accel_group,
                                           accel_key=gtk.gdk.keyval_from_name('c'),
                                           accel_mods=gtk.gdk.MOD1_MASK, accel_flags=0)

        class_c_box.pack_start(child=self.class_c_check, expand=False, fill=False, padding=0)

        class_box.pack_start(child=class_c_box, expand=False, fill=False, padding=5)

        # ----------------------------------------------------------- #

        self._content_area.pack_start(child=class_frame, expand=False, fill=False, padding=10)

    def _generate_timing_container(self):
        """
        Generate the container which will implement a timer to
        count-down or count-up depending on the user's preference.
        """
        timer_frame = gtk.Frame(label=" Timer ")
        timer_frame.set_shadow_type(type=gtk.SHADOW_ETCHED_IN)
        timer_box = gtk.HBox()
        timer_frame.add(timer_box)

        # ----------------------------------------------------------- #
        enable_label = gtk.Label()
        enable_label.set_text_with_mnemonic("_Enable Timer:")

        self.enable_timer_check = gtk.CheckButton()
        self.enable_timer_check.connect("toggled", self._timer_enabled_checkbutton_toggled)

        enable_label.set_mnemonic_widget(widget=self.enable_timer_check)

        timer_accel_group = gtk.AccelGroup()
        self.add_accel_group(timer_accel_group)
        self.enable_timer_check.add_accelerator(accel_signal="clicked",
                                                accel_group=timer_accel_group,
                                                accel_key=gtk.gdk.keyval_from_name('e'),
                                                accel_mods=gtk.gdk.MOD1_MASK, accel_flags=0)

        timer_box.pack_start(child=enable_label, expand=False, fill=False, padding=0)
        timer_box.pack_start(child=self.enable_timer_check, expand=False, fill=False, padding=0)

        # ----------------------------------------------------------- #
        timer_adjust = gtk.Adjustment(value=15, lower=1, upper=60, step_incr=1, page_incr=5)
        self.timer_spin = gtk.SpinButton(adjustment=timer_adjust)
        self.timer_spin.set_value(value=15)
        timer_box.pack_start(child=self.timer_spin, expand=False, fill=False, padding=5)

        self._content_area.pack_start(child=timer_frame, expand=False, fill=False, padding=5)

    def _generate_network_to_guess_container(self):
        """
        Generate the container which will be used to display the
        network to be guess by the user.
        """
        network_box = gtk.HBox()

        self.network_to_guess_label = gtk.Label("NETWORK TO GUESS GOES HERE!")
        network_box.pack_start(child=self.network_to_guess_label, expand=True, fill=False,
                               padding=5)

        self.new_network_button = gtk.Button("New Network")
        self.new_network_button.connect("clicked", self._new_network_button_clicked)

        new_group = gtk.AccelGroup()
        self.add_accel_group(new_group)
        self.new_network_button.add_accelerator(accel_signal="clicked", accel_group=new_group,
                                                accel_key=gtk.gdk.keyval_from_name('n'),
                                                accel_mods=gtk.gdk.CONTROL_MASK, accel_flags=0)

        network_box.pack_start(child=self.new_network_button, expand=False, fill=False, padding=5)

        self._content_area.pack_start(child=network_box, expand=False, fill=False, padding=5)

    def _generate_guess_container(self):
        """
        Generate the container which will be used to for the user to
        input their guess.
        """
        guess_grid = gtk.Table(rows=6, columns=6, homogeneous=False)

        # ----------------------------------------------------------- #
        network_label = gtk.Label("Network: ")
        guess_grid.attach(child=network_label, left_attach=0, right_attach=1, top_attach=0,
                          bottom_attach=1)

        self.network_guess_entry = gtk.Entry()
        self.network_guess_entry.connect("activate", self._text_entry_activate)
        guess_grid.attach(child=self.network_guess_entry, left_attach=1, right_attach=5,
                          top_attach=0, bottom_attach=1)

        self.network_image = gtk.Image()
        self.network_image.set_from_stock(gtk.STOCK_REMOVE, gtk.ICON_SIZE_MENU)
        guess_grid.attach(child=self.network_image, left_attach=5, right_attach=6,
                          top_attach=0, bottom_attach=1)

        # ----------------------------------------------------------- #
        netmask_label = gtk.Label("Subnet Mask: ")
        guess_grid.attach(child=netmask_label, left_attach=0, right_attach=1, top_attach=1,
                          bottom_attach=2)

        self.netmask_guess_entry = gtk.Entry()
        self.netmask_guess_entry.connect("activate", self._text_entry_activate)
        guess_grid.attach(child=self.netmask_guess_entry, left_attach=1, right_attach=5,
                          top_attach=1, bottom_attach=2)

        self.netmask_image = gtk.Image()
        self.netmask_image.set_from_stock(gtk.STOCK_REMOVE, gtk.ICON_SIZE_MENU)
        guess_grid.attach(child=self.netmask_image, left_attach=5, right_attach=6,
                          top_attach=1, bottom_attach=2)

        # ----------------------------------------------------------- #
        broadcast_label = gtk.Label("Broadcast Address:")
        guess_grid.attach(child=broadcast_label, left_attach=0, right_attach=1, top_attach=2,
                          bottom_attach=3)

        self.broadcast_guess_entry = gtk.Entry()
        self.broadcast_guess_entry.connect("activate", self._text_entry_activate)
        guess_grid.attach(child=self.broadcast_guess_entry, left_attach=1, right_attach=5,
                          top_attach=2, bottom_attach=3)

        self.broadcast_image = gtk.Image()
        self.broadcast_image.set_from_stock(gtk.STOCK_REMOVE, gtk.ICON_SIZE_MENU)
        guess_grid.attach(child=self.broadcast_image, left_attach=5, right_attach=6,
                          top_attach=2, bottom_attach=3)

        # ----------------------------------------------------------- #
        usable_host_label = gtk.Label("Usable Host Addresses: ")
        guess_grid.attach(child=usable_host_label, left_attach=0, right_attach=1, top_attach=3,
                          bottom_attach=4)

        self.usable_guess_entry = gtk.Entry()
        self.usable_guess_entry.connect("activate", self._text_entry_activate)
        guess_grid.attach(child=self.usable_guess_entry, left_attach=1, right_attach=5,
                          top_attach=3, bottom_attach=4)

        self.usable_image = gtk.Image()
        self.usable_image.set_from_stock(gtk.STOCK_REMOVE, gtk.ICON_SIZE_MENU)
        guess_grid.attach(child=self.usable_image, left_attach=5, right_attach=6,
                          top_attach=3, bottom_attach=4)

        # ----------------------------------------------------------- #
        self.check_guess_button = gtk.Button("Check Answers")
        self.check_guess_button.connect("clicked", self._check_guess_button_clicked)
        guess_grid.attach(child=self.check_guess_button, left_attach=5, right_attach=6,
                          top_attach=4, bottom_attach=5)

        # ----------------------------------------------------------- #
        self.reveal_answer_button = gtk.Button("Reveal Answers")
        self.reveal_answer_button.connect("clicked", self._reveal_answer_button_clicked)

        reveal_group = gtk.AccelGroup()
        self.add_accel_group(reveal_group)
        self.reveal_answer_button.add_accelerator(accel_signal="clicked", accel_group=reveal_group,
                                                  accel_key=gtk.gdk.keyval_from_name('r'),
                                                  accel_mods=gtk.gdk.CONTROL_MASK, accel_flags=0)

        guess_grid.attach(child=self.reveal_answer_button, left_attach=5, right_attach=6,
                          top_attach=5, bottom_attach=6)

        self._content_area.pack_start(child=guess_grid, expand=False, fill=True, padding=5)

    ###########################################################################
    #                                CALLBACKS                                #
    ###########################################################################
    def _class_checkbutton_toggled(self, widget, name):
        """
        Callback for the class CheckButtons. Add/remove the
        """
        if widget.get_active():
            self.class_check_list.append(name)
        else:
            self.class_check_list.remove(name)

    def _timer_enabled_checkbutton_toggled(self, widget, event=None):
        """
        Callback for the enable_timer CheckButton.
        """
        print event

    def _new_network_button_clicked(self, widget, event=None):
        """
        Callback for the "New Network" button. Used to generate a new
        network for the user to guess.
        """
        self._generate_network_to_guess()

    def _text_entry_activate(self, widget, event=None):
        """
        Callback for when the return key is pressed when a text entry
        has focus.
        """
        self._check_guess()

    def _check_guess_button_clicked(self, widget, event=None):
        """
        Check the guesses in the text entry boxes when the button is
        is clicked.
        """
        self._check_guess()

    def _reveal_answer_button_clicked(self, widget, event=None):
        """
        Callback to reveal the answers when the answer button is
        clicked.
        """
        self._reveal_answers()

    ###########################################################################
    #                                 METHODS                                 #
    ###########################################################################
    def _generate_network_to_guess(self):
        """
        Generate the network for the user to guess. Set the
        network_to_guess_label to this value.
        """
        self._reset_images()
        self._clear_text_entries()

        # get the class that will be used to generate the host within
        # a network to guess.
        list_len = len(self.class_check_list)

        # if the length is 0, no class has been selected, return for
        # now, deal with it later.
        if list_len == 0:
            return "0.0.0.0/0"

        index = 0 if list_len == 1 else random.randrange(start=0, stop=list_len)
        the_class = self.class_check_list[index]

        if the_class == "class_a":
            network_class = class_a
        elif the_class == "class_b":
            network_class = class_b
        else:
            network_class = class_c

        cidr_value = random.randrange(start=network_class.lowest_cidr, stop=UPPER_CIDR_VALUE+1)

        # list containing the four network octets, will be concatenated
        # to provide the host.
        network_address_octets = []

        network_address_octets.append(network_class.generate_first_octet())
        for i in range(1, 4):
            network_address_octets.append(self._generate_octet())

        network_address = ("{oct0}.{oct1}.{oct2}.{oct3}/{cidr}"
                           .format(oct0=network_address_octets[0], oct1=network_address_octets[1],
                                   oct2=network_address_octets[2], oct3=network_address_octets[3],
                                   cidr=cidr_value))

        self.network_to_guess_label.set_text(network_address)

        self.answer = Answer(network_address)

        # set the cursor focus to the network entry.
        self.network_guess_entry.grab_focus()

    @staticmethod
    def _generate_octet():
        """
        Generate a value between 0 and 255.

        @rtype: int
        @return: Integer between 0 and 255 to be used for an octet.
        """
        return random.randrange(start=LOWER_OCTET_VALUE, stop=UPPER_OCTET_VALUE+1)

    def _reset_images(self):
        """
        Reset the images next to the test entries.
        """
        self.network_image.set_from_stock(gtk.STOCK_REMOVE, gtk.ICON_SIZE_MENU)
        self.netmask_image.set_from_stock(gtk.STOCK_REMOVE, gtk.ICON_SIZE_MENU)
        self.broadcast_image.set_from_stock(gtk.STOCK_REMOVE, gtk.ICON_SIZE_MENU)
        self.usable_image.set_from_stock(gtk.STOCK_REMOVE, gtk.ICON_SIZE_MENU)

    def _clear_text_entries(self):
        """
        When a new network is generated, clear any text in the guess
        boxes.
        """
        self.network_guess_entry.set_text("")
        self.netmask_guess_entry.set_text("")
        self.broadcast_guess_entry.set_text("")
        self.usable_guess_entry.set_text("")

    def _check_guess(self):
        """
        Check the guesses in the text entry boxes to see if they match
        the values in the Answer class.
        """
        user_network = self.network_guess_entry.get_text()
        user_netmask = self.netmask_guess_entry.get_text()
        user_broadcast = self.broadcast_guess_entry.get_text()
        user_usable_hosts = self.usable_guess_entry.get_text()

        if user_network == self.answer.network:
            self.network_image.set_from_stock(gtk.STOCK_APPLY, gtk.ICON_SIZE_MENU)
        else:
            self.network_image.set_from_stock(gtk.STOCK_REMOVE, gtk.ICON_SIZE_MENU)

        if user_netmask == self.answer.netmask:
            self.netmask_image.set_from_stock(gtk.STOCK_APPLY, gtk.ICON_SIZE_MENU)
        else:
            self.netmask_image.set_from_stock(gtk.STOCK_REMOVE, gtk.ICON_SIZE_MENU)

        if user_broadcast == self.answer.broadcast:
            self.broadcast_image.set_from_stock(gtk.STOCK_APPLY, gtk.ICON_SIZE_MENU)
        else:
            self.broadcast_image.set_from_stock(gtk.STOCK_REMOVE, gtk.ICON_SIZE_MENU)

        if user_usable_hosts == self.answer.usable_hosts:
            self.usable_image.set_from_stock(gtk.STOCK_APPLY, gtk.ICON_SIZE_MENU)
        else:
            self.usable_image.set_from_stock(gtk.STOCK_REMOVE, gtk.ICON_SIZE_MENU)

    def _reveal_answers(self):
        """
        Reveal the answers by putting the correct information in the
        text entry fields.
        """
        self.network_guess_entry.set_text(self.answer.network)
        self.netmask_guess_entry.set_text(self.answer.netmask)
        self.broadcast_guess_entry.set_text(self.answer.broadcast)
        self.usable_guess_entry.set_text(self.answer.usable_hosts)

if __name__ == "__main__":
    SubnetTester()
    gtk.main()
