import sys
import re

replacements = {
    '(void)': '()',
    'void*': 'void*',
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
    if name.startswith("glfw"):
        name = name[4:]
        name = name[0].lower() + name[1:]
        return name
    return name

special = {
    'glfwGetKeyName',
    'glfwGetJoystickName',
    'glfwGetJoystickGUID',
    'glfwUpdateGamepadMappings',
    'glfwGetGamepadName',
    'glfwSetClipboardString',
    'glfwGetClipboardString',
    'glfwExtensionSupported',
    'glfwGetProcAddress',
    'glfwGetRequiredInstanceExtensions',
    'glfwGetVersionString',
    'glfwGetError',
    'glfwGetMonitorName',
    'glfwWindowHintString',
    'glfwCreateWindow',
    'glfwGetWindowTitle',
    'glfwSetWindowTitle'
}

with open(sys.argv[2], "w") as out:
    natives = ''
    nicenames = ''
    with open(sys.argv[1], "r") as f:
        for line in f.readlines():
            line = line.lstrip()
            if line.startswith("GLFWAPI "):
                lparen = line.index('(')
                rparen = line.index(')')
                params = line[lparen:rparen + 1]
                parameterNames = []
                paramComponents = filter(lambda x: len(x) > 0, re.split(r'[\(\)\,]', params))
                for var in paramComponents:
                    paramNameIndex = len(var) - 1
                    while paramNameIndex >= 0 and not var[paramNameIndex].isspace() and var[paramNameIndex] != '*':
                        paramNameIndex -= 1
                    if paramNameIndex >= 0:
                        parameterNames.append(var[paramNameIndex + 1:])

                namestart = lparen - 1
                while not line[namestart].isspace() and line[namestart] != '*':
                    namestart -= 1
                name = line[namestart + 1:lparen]

                returnType = line[8:namestart]

                quotedName = f"`{name}`"
                niceName = adaptName(name)

                nativeDef = f'        {returnType} {quotedName}{params}\n'
                niceDef = f'    {returnType} {niceName}{params}: native.{name}({', '.join(parameterNames)})\n'
                if 'VK' in nativeDef or 'vk' in nativeDef or 'Vk' in nativeDef:
                    continue
                for k, v in replacements.items():
                    nativeDef = nativeDef.replace(k, v, -1)
                    niceDef = niceDef.replace(k, v, -1)

                natives += nativeDef
                if name not in special:
                    nicenames += niceDef
    out.write('    in native:\n')
    out.write(natives)
    out.write(nicenames)
