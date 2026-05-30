import sys

replacements = {
    '(void)': '()',
    'void*': 'i8*',
    'const unsigned char': 'u8',
    'const char': 'i8',
    'char ': 'i8 ',
    'unsigned char': 'u8',
    'unsigned int': 'u32',
    'uint64_t': 'u64',
    'uint32_t': 'u32',
    'int ': 'i32 ',
    'int*': 'i32*',
    'const float': 'f32',
    'float ': 'f32 ',
    'double ': 'f64 ',
    'float*': 'f32*',
    'double*': 'f64*',
    'GLFWglproc': 'Glproc',
    'GLFWvkproc': 'Vkproc',
    'GLFWmonitor': 'Monitor',
    'GLFWwindow': 'Window',
    'GLFWcursor': 'Cursor',
    'GLFWallocatefun': 'Allocatefun',
    'GLFWreallocatefun': 'Reallocatefun',
    'GLFWdeallocatefun': 'Deallocatefun',
    'GLFWerrorfun': 'Errorfun',
    'GLFWwindowposfun': 'Windowposfun',
    'GLFWwindowsizefun': 'Windowsizefun',
    'GLFWwindowclosefun': 'Windowclosefun',
    'GLFWwindowrefreshfun': 'Windowrefreshfun',
    'GLFWwindowfocusfun': 'Windowfocusfun',
    'GLFWwindowiconifyfun': 'Windowiconifyfun',
    'GLFWwindowmaximizefun': 'Windowmaximizefun',
    'GLFWframebuffersizefun': 'Framebuffersizefun',
    'GLFWwindowcontentscalefun': 'Windowcontentscalefun',
    'GLFWmousebuttonfun': 'Mousebuttonfun',
    'GLFWcursorposfun': 'Cursorposfun',
    'GLFWcursorenterfun': 'Cursorenterfun',
    'GLFWscrollfun': 'Scrollfun',
    'GLFWkeyfun': 'Keyfun',
    'GLFWcharfun': 'Charfun',
    'GLFWcharmodsfun': 'Charmodsfun',
    'GLFWdropfun': 'Dropfun',
    'GLFWmonitorfun': 'Monitorfun',
    'GLFWjoystickfun': 'Joystickfun',
    'const GLFWvidmode': 'Vidmode',
    'const GLFWgammaramp': 'Gammaramp',
    'const GLFWimage': 'Image',
    'const GLFWgamepadstate': 'Gamepadstate',
    'const GLFWallocator': 'Allocator',
    'GLFWvidmode': 'Vidmode',
    'GLFWgammaramp': 'Gammaramp',
    'GLFWimage': 'Image',
    'GLFWgamepadstate': 'Gamepadstate',
    'GLFWallocator': 'Allocator',
    ';': ''
}

modifiers = {
    'const', 'unsigned'
}

def adaptName(name):
    name = name.lstrip("(").rstrip(")")
    if name.startswith("GLFW_"):
        return name[5:] # strip off the GLFW_ part
    return name

with open(sys.argv[2], "w") as out:
    out.write("use glfwtypes\n")
    out.write("in glfw:\n")
    with open(sys.argv[1], "r") as f:
        for line in f.readlines():
            line = line.lstrip()
            if line.startswith("GLFWAPI "):
                terms = line.split()
                name = 2
                while terms[name - 1] in modifiers:
                    name += 1
                nameparts = terms[name].split('(')
                nameparts[0] = f"`{nameparts[0]}`"
                terms[name] = nameparts[0] + '(' + nameparts[1]
                result = ' '.join(terms[1:])
                for k, v in replacements.items():
                    result = result.replace(k, v, -1)
                if 'vk' in result or 'Vk' in result:
                    result = "# " + result
                out.write('    ' + result + '\n')
