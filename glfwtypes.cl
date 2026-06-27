use std/maybe, std/rt

in glfw:
    alias Glproc: void*
    alias Vkproc: void*

    type Monitor
    type Window
    type Cursor

    alias Allocatefun: i8*(u64, i8*)
    alias Reallocatefun: i8*(i8*, u64, i8*)
    alias Deallocatefun: void(i8*, i8*)
    alias Errorfun: void(i32, i8*)
    alias Windowposfun: void(Window*, i32, i32)
    alias Windowsizefun: void(Window*, i32, i32)
    alias Windowclosefun: void(Window*)
    alias Windowrefreshfun: void(Window*)
    alias Windowfocusfun: void(Window*, i32)
    alias Windowiconifyfun: void(Window*, i32)
    alias Windowmaximizefun: void(Window*, i32)
    alias Framebuffersizefun: void(Window*, i32, i32)
    alias Windowcontentscalefun: void(Window*, f32, f32)
    alias Mousebuttonfun: void(Window*, i32, i32, i32)
    alias Cursorposfun: void(Window*, f64, f64)
    alias Cursorenterfun: void(Window*, i32)
    alias Scrollfun: void(Window*, f64, f64)
    alias Keyfun: void(Window*, i32, i32, i32, i32)
    alias Charfun: void(Window*, u32)
    alias Charmodsfun: void(Window*, u32, i32)
    alias Dropfun: void(Window*, i32, i8**)
    alias Monitorfun: void(Monitor*, i32)
    alias Joystickfun: void(i32, i32)

    type Vidmode:
        i32 width, height
        i32 redBits, greenBits, blueBits
        i32 refreshRate

    type Gammaramp:
        u16* red, green, blue
        u32 size

    type Image:
        i32 width, height
        u8* pixels

    type Gamepadstate:
        u8[15] buttons
        f32[6] axes

    type Allocator:
        Allocatefun allocate
        Reallocatefun reallocate
        Deallocatefun deallocate
        i8* user
