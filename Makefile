glfwconsts.cl: glfw/include/GLFW/glfw3.h genconsts.py
	python3 genconsts.py $< $@
glfwfuncs.cl: glfw/include/GLFW/glfw3.h genfuncs.py
	python3 genfuncs.py $< $@

glfw.cl: glfwtypes.cl glfwconsts.cl glfwfuncs.cl glfwspecialfuncs.cl
	cat $^ > $@

clean:
	rm -f *.o glfwconsts.cl glfwfuncs.cl glfw.cl
