from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

# qtile cmd-obj -o cmd -f reload_config

mod = "mod4"
terminal = guess_terminal()

group_names = "asdfzxcv"
groups = [Group(i) for i in group_names]


direction_order = ["left", "up", "down", "right"]
direction_keys = "asdf"
direction_keys_display = "   ".join([f"[{key}] {direction}" for direction, key in zip(direction_order, direction_keys)])

focus_windows = [lazy.layout.left, lazy.layout.up, lazy.layout.down, lazy.layout.right]
move_windows = [lazy.layout.shuffle_left, lazy.layout.shuffle_up, lazy.layout.shuffle_down, lazy.layout.shuffle_right]
grow_windows = [lazy.layout.grow_left, lazy.layout.grow_up, lazy.layout.grow_down, lazy.layout.grow_right]

switch_group = lambda g: lazy.group[g.name].toscreen()
move_switch_group = lambda g: lazy.window.togroup(g.name, switch_group=True)
move_group = lambda g: lazy.window.togroup(g.name)

keys = [
    KeyChord([], "Super_L", [
        Key([], "v", lazy.spawn("xsecurelock"), desc="Logout"),
        Key([], "z", lazy.shutdown(), desc="Logout"),

        Key([], "Return", lazy.spawn("rofi -show drun"), desc="Rofi"),

        Key([], "b", lazy.window.kill(), desc="Close"),
        KeyChord([], "d", mode=True, name=f"Focus   {direction_keys_display}",
                 submappings=[Key([], key, cmd()) for key, cmd in zip(direction_keys, focus_windows)]),
        KeyChord([], "s", mode=True, name=f"Move   {direction_keys_display}",
                 submappings=[Key([], key, cmd()) for key, cmd in zip(direction_keys, move_windows)]),
        KeyChord([], "w", mode=True, name=f"Grow   {direction_keys_display}",
                 submappings=[Key([], key, cmd()) for key, cmd in zip(direction_keys, grow_windows)]),

        KeyChord([], "f", name="Switch",
                 submappings=[Key([], g.name, switch_group(g)) for g in groups]),
        KeyChord([], "a", name="Place+Switch",
                 submappings=[Key([], g.name, move_switch_group(g)) for g in groups]),
        KeyChord([], "g", name="Place",
                 submappings=[Key([], g.name, move_group(g)) for g in groups]),
    ], name="v Lock / z Logout / ↵ Rofi / b Close / d Focus / s Move / f Switch / g Place / a Place+Switch / w Grow"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    # Toggle between different layouts as defined below
    # Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
]

layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(),
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

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.Spacer(20),
                widget.GroupBox(),
                widget.Spacer(20),
                widget.Sep(),
                widget.Chord(foreground='00cc00'),
                widget.Spacer(),
                widget.Sep(),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.Systray(),
                widget.Clock(format="%Y-%m-%d %a %I:%M %p"),
            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# Allows apps to request auto-minimizing when focus is lost
auto_minimize = True
# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None
# Needed for Java UI toolkits
wmname = "LG3D"

