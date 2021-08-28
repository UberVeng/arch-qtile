# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess

from typing import List  # noqa: F401
from itertools import cycle

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, KeyChord
from libqtile.lazy import lazy

mod = "mod4"
# terminal = guess_terminal()
terminal = "kitty"
gapSize = 15 
gapToggle = [0, 15]
gap = cycle(gapToggle)

@lazy.function
def Maximize(qtile):
    lazy.next_layout(),
    gapSize = next(gap)
   

keys = [

    #Key([mod], "space", lazy.widget["keyboardlayout"].next_keyboard())
    #Key(["alt", "space"], lazy.widget["keyboardlayout"].next_keyboard(), desc="Next keyboard layout."),
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod, "mod1"], "space", lazy.layout.next(), desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod, "shift"], "z", lazy.window.toggle_floating(), desc="Toggle floating mode"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    #Key([mod], "space", lazy.function(Maximize), desc="Toggle between layouts"),
    Key([mod], "space", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key(["mod1"],"Tab", lazy.widget["keyboardlayout"].next_keyboard(), desc="Next keyboard layout."),
	Key([], "Print", lazy.spawn("scrot '%Y-%m-%d-%s_screenshot_$wx$h.png' -e 'mv $f ~/Pictures/screenshots/'")),
	Key(["mod1"], "Print", lazy.spawn("scrot '%Y-%m-%d-%s_screenshot_$wx$h.png' -e 'mv $f ~/Pictures/screenshots/'")),


    Key([mod], "z", lazy.to_screen(0), desc='Keyboard focus to monitor 1'),
    Key([mod], "x", lazy.to_screen(1), desc='Keyboard focus to monitor 2'),

    #keyChords
    KeyChord(["mod1"], "e", [
        Key([], "v",
            lazy.spawn("vieb"),
            desc="Launch Vieb browser"
            ),
        Key([], "q",
            lazy.spawn("qtox"),
            desc="Launch qTox"
            )
        ]),
]

# Group name: key bind
group_names = {
	'WWW': 'Tab',
	'DEV': 'a',
	'SYS': 's',
	'GFX': 'd',
	'ETC': 'f',
	'VBX': 'g'
}
groups = [Group(name, layout='column') for name in group_names]
for name in group_names:
	keys += [
		Key([mod], group_names[name], lazy.group[name].toscreen()),
		Key([mod, 'shift'], group_names[name], lazy.window.togroup(name))]

layout_theme = {"border_width": 6,
                "margin": [0, 0, gapSize, gapSize],
                "border_focus": "ab8b82",
                "border_normal": "e7cf93",
                "border_normal_stack": "e7cf93",
                "border_on_single": True,
                "fullscreen_border_width": 0,
                "max_border_width": 0,
                "insert_position": 1
                }

layout_float = {"border_focus": "ab8b82",
                "border_normal": "e7cf93",
                "border_width": 6,
                "fullscreen_border_width": 6,
                "max_border_width": 6
                }
bar_config = {
        "margin": gapSize
			}
layouts = [
    layout.Columns(**layout_theme),
    layout.Max(**layout_theme),
    # layout.Floating(**layout_float)
    # layout.Matrix(**layout_theme)
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

color = {'bg': '#7a635d',
        'fg': 'b8958c',
        'semi-light': 'e5d8b1',
        'fg-light': 'e3d4ad',
        'fg-dark': '423431',
        'bg-dark': '664f4f',
        'selected': 'dbca9f',
        'red': 'ff9978',
        'dark-red':'bb4f58',
        'green': '247d4a',
        'blue': '228a93'
        } 

widget_defaults = dict(
    background = color['bg'],
    font='Ubuntu Regular',
    fontsize=12,
    padding = 3,
)



extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
        [
                widget.Sep(
                    linewidth = 0,
                    padding = 8,
                    ),
                widget.GroupBox(
                    font = 'Ubuntu Bold',
                    fontsize = 14,
                    active = color['fg'],
                    inactive = color['fg-dark'], 

                    #current workspace on current screen
                    this_current_screen_border = color['fg-light'],

                    #current workspace on inactive screen
                    other_current_screen_border = color['bg-dark'],
                    this_screen_border = color['dark-red'],
                    other_screen_border = color['bg-dark'],
                    padding_x = 10,
                    padding_y = 15,
                    margin_y = 5,
                    margin_x = 0,
                    disable_drag = True,
                    highlight_method = "block",
                    rounded = False,
                    urgent_alert_method =  "text",
                    urgent_text = color['red'],
                    ),
                widget.Sep(
                    linewidth = 0,
                    padding = 5,
                    ),
                widget.CurrentLayout(
                    font='Ubuntu Bold',
                    fontsize = 14,
                    foreground = color['fg-light'],
                    fmt = ('{:.3}'),
                    ),
                widget.Prompt(
                    font='Ubuntu Bold',
                    fontsize = 14,
                    foreground = color['fg-light'],
                    prompt = ':  ',
                    ),
                widget.Spacer(),

                widget.Clock(
                    font = 'Ubuntu Bold',
                    fontsize = 14,
                    foreground = color['fg-light'],
                    format='%A  %d.%m.%Y  %H:%M'
                    ),

                widget.Spacer(),
                
                widget.Chord(
                    chords_colors={
                       'launch': (color['bg'], color['fg']),
                    },
                    font = 'Ubuntu Bold',
                    fontsize = '14',
                    name_transform=lambda name: name.upper(),
                    max_chars = 10,
                ),
				widget.Systray(
					icon_size = 16,
					padding = 5 
				),
                widget.Cmus(
                    font = 'Ubuntu Bold',
                    fontsize = '14',
                    foreground = color['fg-light'],
                    noplay_color = color['fg'],
                    play_color = color['fg-light'],
                    padding = 7,
                    max_chars = 25
                    ),
                widget.OpenWeather(
                        font = 'Ubuntu Bold',
                        fontsize = 14,
                        foreground = color['fg-light'],
                        coordinates = {'longitude': '0', 'latitude': '0'},
                        format = '{main_temp}°{units_temperature} {weather_details}',
                        padding = 7
                        ),
                #widget.CheckUpdates(
                #        font = 'Ubuntu Bold',
                #        fontsize = 14,
                #        foreground = color['fg'],
                #        colour_have_updates = color['fg-light'],
                #        colour_no_updates = color['fg'],
                #        no_update_string = ('no updates'),
                #        update_interval = 1800,
                #        distro = "Arch",
                #        display_format = "{updates} Updates",
                #        mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e sudo pacman -Syu')},
                #        padding = 7
                #        ),
                widget.BitcoinTicker(
                    font = 'Ubuntu Bold',
                    fontsize = 14,
                    foreground = color['fg-light'],
                    update_interval = 20,
                    currency = "USD",
                    padding = 7,
                    fmt = ('{}'),
                    ),
                widget.Sep(
                        linewidth = 0,
                        padding = 7
                        ),
                widget.KeyboardLayout(
                    font = 'Ubuntu Bold',
                    fontsize = 14,
                    background = color['fg-dark'],
                    foreground = color['fg'],
                    configured_keyboards = ['us', 'ru'],
                    padding = 15,
                    
                    ),
                
                widget.Sep(
                    linewidth = 0,
                    padding = 8,
                    ),
                ], 40, **bar_config), right=bar.Gap(size=gapSize),),
    Screen(
        top=bar.Bar(
        [
                widget.Sep(
                    linewidth = 0,
                    padding = 8,
                    ),
                widget.GroupBox(
                    font = 'Ubuntu Bold',
                    fontsize = 14,
                    active = color['fg'],
                    inactive = color['fg-dark'],  
                    this_current_screen_border = color['fg-light'],
                    other_current_screen_border = color['bg-dark'],
                    this_screen_border = color['dark-red'],
                    other_screen_border = color['bg-dark'],
                    padding_x = 10,
                    padding_y = 15,
                    margin_y = 5,
                    margin_x = 0,
                    disable_drag = True,
                    highlight_method = "block",
                    rounded = False,
                    urgent_alert_method =  "text",
                    urgent_text = color['red'],
                    ),
                widget.Sep(
                    linewidth = 0,
                    padding = 5,
                    ),
                widget.CurrentLayout(
                    font='Ubuntu Bold',
                    fontsize = 14,
                    foreground = color['fg-light'],
                    fmt = ('{:.3}'),
                    ),
                widget.Prompt(
                    font='Ubuntu Bold',
                    fontsize = 14,
                    foreground = color['fg-light'],
                    prompt = ':  ',
                    ),
                widget.Spacer(),

                widget.Clock(
                    font = 'Ubuntu Bold',
                    fontsize = 14,
                    foreground = color['fg-light'],
                    format='%A  %d.%m.%Y  %H:%M'
                    ),

                widget.Spacer(),
                widget.Sep(
                        linewidth = 0,
                        padding = 7
                        ),
                widget.KeyboardLayout(
                    font = 'Ubuntu Bold',
                    fontsize = 14,
                    background = color['fg-dark'],
                    foreground = color['fg'],
                    configured_keyboards = ['us', 'ru'],
                    padding = 15,
                    ),
                widget.Sep(
                    linewidth = 0,
                    padding = 8,
                    ),
                ], 40, **bar_config), right=bar.Gap(size=gapSize),),
        ]
    

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
],**layout_float)
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
# wmname = "LG3D"
wmname = "QTile"

# startup apps

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])

@hook.subscribe.client_new
def dialogs(window):
    if window.window.get_wm_type() == 'dialog' or window.window.get_wm_transient_for():
        window.floating = True
