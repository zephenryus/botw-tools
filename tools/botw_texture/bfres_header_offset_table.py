class BFRESHeaderOffsetTable:
    string_pool = 0
    model_dictionary = 0
    texture_dictionary = 0
    skeletal_animation_dictionary = 0
    shader_param_animation_dictionary = 0
    color_animation_dictionary = 0
    tex_srt_anim_dictionary = 0
    tex_pattern_anim_dictionary = 0
    bone_vis_anim_dictionary = 0
    mat_vis_anim_dictionary = 0
    shape_anim_dictionary = 0
    scene_anim_dictionary = 0
    external_file_dictionary = 0

    def __init__(self, string_pool, model_dictionary, texture_dictionary, skeletal_animation_dictionary,
                 shader_param_animation_dictionary, color_animation_dictionary, tex_srt_anim_dictionary,
                 tex_pattern_anim_dictionary, bone_vis_anim_dictionary, mat_vis_anim_dictionary, shape_anim_dictionary,
                 scene_anim_dictionary, external_file_dictionary):
        self.string_pool = string_pool
        self.model_dictionary = model_dictionary
        self.texture_dictionary = texture_dictionary
        self.skeletal_animation_dictionary = skeletal_animation_dictionary
        self.shader_param_animation_dictionary = shader_param_animation_dictionary
        self.color_animation_dictionary = color_animation_dictionary
        self.tex_srt_anim_dictionary = tex_srt_anim_dictionary
        self.tex_pattern_anim_dictionary = tex_pattern_anim_dictionary
        self.bone_vis_anim_dictionary = bone_vis_anim_dictionary
        self.mat_vis_anim_dictionary = mat_vis_anim_dictionary
        self.shape_anim_dictionary = shape_anim_dictionary
        self.scene_anim_dictionary = scene_anim_dictionary
        self.external_file_dictionary = external_file_dictionary

    def __str__(self):
        return "<BFRESHeaderOffsetTable> {{\n\t\tstring_pool: {0},\n\t\tmodel_dictionary: {1},\n\t\t" \
               "texture_dictionary: {2},\n\t\tskeletal_animation_dictionary: {3},\n\t\t" \
               "shader_param_animation_dictionary: {4},\n\t\tcolor_animation_dictionary: {5},\n\t\t" \
               "tex_srt_anim_dictionary: {6},\n\t\ttex_pattern_anim_dictionary: {7},\n\t\t" \
               "bone_vis_anim_dictionary: {8},\n\t\tmat_vis_anim_dictionary: {9},\n\t\t" \
               "shape_anim_dictionary: {10},\n\t\tscene_anim_dictionary: {11},\n\t\t" \
               "external_file_dictionary: {12}\n\t}}" \
            .format(
            self.string_pool,
            self.model_dictionary,
            self.texture_dictionary,
            self.skeletal_animation_dictionary,
            self.shader_param_animation_dictionary,
            self.color_animation_dictionary,
            self.tex_srt_anim_dictionary,
            self.tex_pattern_anim_dictionary,
            self.bone_vis_anim_dictionary,
            self.mat_vis_anim_dictionary,
            self.shape_anim_dictionary,
            self.scene_anim_dictionary,
            self.external_file_dictionary,
        )
