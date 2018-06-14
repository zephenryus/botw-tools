class BFRESHeaderCountTable:
    model = 0
    texture = 0
    skeletal_anim = 0
    shader_param_anim = 0
    color_anim = 0
    tex_srt_anim = 0
    tex_pattern_anim = 0
    bone_vis_anim = 0
    mat_vis_anim = 0
    scene_anim = 0
    external_file = 0

    def __init__(self, model, texture, skeletal_anim, shader_param_anim, color_anim, tex_srt_anim, tex_pattern_anim,
                 bone_vis_anim, mat_vis_anim, scene_anim, external_file):
        self.model = model
        self.texture = texture
        self.skeletal_anim = skeletal_anim
        self.shader_param_anim = shader_param_anim
        self.color_anim = color_anim
        self.tex_srt_anim = tex_srt_anim
        self.tex_pattern_anim = tex_pattern_anim
        self.bone_vis_anim = bone_vis_anim
        self.mat_vis_anim = mat_vis_anim
        self.scene_anim = scene_anim
        self.external_file = external_file

    def __str__(self):
        return "<BFRESHeaderCountTable> {{\n\t\tmodel: {0},\n\t\ttexture: {1},\n\t\tskeletal_anim: {2},\n\t\tshader_param_anim: {3},\n\t\tcolor_anim: {4},\n\t\ttex_srt_anim: {5},\n\t\ttex_pattern_anim: {6},\n\t\tbone_vis_anim: {7},\n\t\tmat_vis_anim: {8},\n\t\tscene_anim: {9},\n\t\texternal_file: {10}\n\t}}" \
            .format(
            self.model,
            self.texture,
            self.skeletal_anim,
            self.shader_param_anim,
            self.color_anim,
            self.tex_srt_anim,
            self.tex_pattern_anim,
            self.bone_vis_anim,
            self.mat_vis_anim,
            self.scene_anim,
            self.external_file
        )
