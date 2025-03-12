import moderngl_window as mglw

class app(mglw.WindowConfig):
    window_size=1600,900
    resource_dir = 'programs'

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        #plain with 4 vertices
        self.quad = mglw.geometry.quad_fs()
        #load shader program
        self.prog = self.load_program(vertex_shader='vertex_shader.glsl',
                                      fragment_shader='fragment_shader.glsl')
        
        self.set_uniform('resolution',self.window_size)
        
    def set_uniform(self, u_name, u_value):
        try:
            self.prog[u_name] = u_value
        except KeyError:
            print(f'uniform: {u_name} - not used in shader')

    def render(self,time,from_time):
        self.ctx.clear()
        self.set_uniform('time',time)
        self.quad.render(self.prog)

if __name__ == '__main__':
    mglw.run_window_config(app)