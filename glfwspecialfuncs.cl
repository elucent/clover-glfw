    i64 ptrToInt(type T, T* ptr):
        i64 i: 0
        memory.move(&i, &ptr, |i64|)
        return i

    T* intToPtr(type T, i64 i):
        T* ptr: uninit
        memory.move(&ptr, &i, |i64|)
        return ptr

    i8[] fromCString(i8* ptr):
        type Slice:
            i8* ptr
            u64 size
        var slice: Slice(ptr, 0)
        while *ptr != 0:
            slice.size ++
            ptr = (ptrToInt(ptr) + |i8|).intToPtr(i8)
        i8[] result: uninit
        memory.move(&result, &slice, |Slice|)
        return result

    bool isCString?(i8[] str):
        return str[|str| - 1] == 0

    own i8[] toCString(i8[] str):
        var result: new i8[|str| + 1]
        result[:|str|] = str
        result[|str|] = 0
        return result as own i8[]

    i8[] getVersionString():
        fromCString(native.glfwGetVersionString())
    i8[] getMonitorName(Monitor* monitor):
        fromCString(native.glfwGetMonitorName(monitor))
    i8[] getWindowTitle(Window* window):
        fromCString(native.glfwGetWindowTitle(window))
    i8[] getKeyName(i32 key, i32 scancode):
        fromCString(native.glfwGetKeyName(key, scancode))
    i8[] getJoystickName(i32 jid):
        fromCString(native.glfwGetJoystickName(jid))
    i8[] getJoystickGUID(i32 jid):
        fromCString(native.glfwGetJoystickGUID(jid))
    i8[] getGamepadName(i32 jid):
        fromCString(native.glfwGetGamepadName(jid))
    i8[] getClipboardString(Window* window):
        fromCString(native.glfwGetClipboardString(window))

    (i32, i8[]) getError():
        i8* ptr: uninit
        i32 result: native.glfwGetError(&ptr)
        return (result, fromCString(ptr))

    own i8[][] getRequiredInstanceExtensions():
        u32 numStrings: 0
        i8** nativeStr: native.glfwGetRequiredInstanceExtensions(&numStrings)
        var result: new i8[][numStrings]
        for i < numStrings:
            i8* str: *intToPtr(i8*, ptrToInt(nativeStr) + i * |i64|)
            result[i] = fromCString(str)
        return result as own i8[][]

    void windowHintString(i32 hint, i8[] value):
        if value.isCString?():
            native.glfwWindowHintString(hint, &value[0])
        else:
            var copy: value.toCString()
            native.glfwWindowHintString(hint, &copy[0])

    Window* createWindow(i32 width, i32 height, i8[] title, Maybe(Monitor*) monitor, Maybe(Window*) share):
        Monitor* passedMonitor: uninit
        Window* passedShare: uninit
        i64 zero: 0
        if monitor is Some(ptr):
            passedMonitor = ptr
        else:
            memory.move(&passedMonitor, &zero, |i64|)
        if share is Some(ptr):
            passedShare = ptr
        else:
            memory.move(&passedShare, &zero, |i64|)
        if title.isCString?():
            return native.glfwCreateWindow(width, height, &title[0], passedMonitor, passedShare)
        var copy: title.toCString()
        return native.glfwCreateWindow(width, height, &copy[0], passedMonitor, passedShare)

    void setWindowTitle(Window* window, i8[] title):
        if title.isCString?():
            native.glfwSetWindowTitle(window, &title[0])
        else:
            var copy: title.toCString()
            native.glfwSetWindowTitle(window, &copy[0])

    i32 updateGamepadMappings(i8[] string):
        if string.isCString?():
            return native.glfwUpdateGamepadMappings(&string[0])
        var copy: string.toCString()
        return native.glfwUpdateGamepadMappings(&copy[0])

    void setClipboardString(Window* window, i8[] string):
        if string.isCString?():
            native.glfwSetClipboardString(window, &string[0])
        else:
            var copy: string.toCString()
            native.glfwSetClipboardString(window, &copy[0])

    i32 extensionSupported(i8[] string):
        if string.isCString?():
            return native.glfwExtensionSupported(&string[0])
        var copy: string.toCString()
        return native.glfwExtensionSupported(&copy[0])

    Glproc getProcAddress(i8[] string):
        if string.isCString?():
            return native.glfwGetProcAddress(&string[0])
        var copy: string.toCString()
        return native.glfwGetProcAddress(&copy[0])
