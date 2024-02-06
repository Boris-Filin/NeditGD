
# This class is put on hold until later updates
class Emitter():
    def __init__(self):
        # Implement defaults later
        pass

    @classmethod
    def from_string(cls, data: str):
        emitter = cls()
        vals = data.split('a')

        emitter.max_particles = float(vals[0])
        emitter.duration = float(vals[1])
        emitter.lifetime = float(vals[2])
        emitter.lifetime_range = float(vals[3])
        emitter.emission = float(vals[4])
        emitter.angle = float(vals[5])
        emitter.angle_range = float(vals[6])
        emitter.speed = float(vals[7])
        emitter.speed_range = float(vals[8])
        emitter.pos_var_x = float(vals[9])
        emitter.pos_var_y = float(vals[10])
        emitter.gravity_x = float(vals[11])
        emitter.gravity_y = float(vals[12])
        emitter.accel_rad = float(vals[13])
        emitter.accel_rad_range = float(vals[14])
        emitter.accel_tan = float(vals[15])
        emitter.accel_tan_range = float(vals[16])

        emitter.start_rad = float(vals[45])
        emitter.start_rad_range = float(vals[46])
        emitter.end_rad = float(vals[47])
        emitter.end_rad_range = float(vals[48])
        emitter.rot_sec = float(vals[49])
        emitter.rot_sec_range = float(vals[50])

        emitter.use_radius = float(vals[51])

        emitter.start_size = float(vals[17])
        emitter.start_size_range = float(vals[18])
        emitter.end_size = float(vals[29])
        emitter.end_size_range = float(vals[30])
        emitter.start_spin = float(vals[19])
        emitter.start_spin_range = float(vals[20])
        emitter.end_spin = float(vals[31])
        emitter.end_spin_range = float(vals[32])

        emitter.start_r = float(vals[21])
        emitter.start_r_range = float(vals[22])
        emitter.start_g = float(vals[23])
        emitter.start_g_range = float(vals[24])
        emitter.start_b = float(vals[25])
        emitter.start_b_range = float(vals[26])
        emitter.start_a = float(vals[27])
        emitter.start_a_range = float(vals[28])
        emitter.end_r = float(vals[33])
        emitter.end_r_range = float(vals[34])
        emitter.end_g = float(vals[35])
        emitter.end_g_range = float(vals[36])
        emitter.end_b = float(vals[37])
        emitter.end_b_range = float(vals[38])
        emitter.end_a = float(vals[39])
        emitter.end_a_range = float(vals[40])

        emitter.free_relative_grouped = float(vals[52])

        emitter.additive = float(vals[53])
        emitter.start_eq_end_spin = float(vals[54])
        emitter.start_rot_is_dir = float(vals[55])
        emitter.dynamic_rotation = float(vals[56])
        emitter.uniform_obj_color = float(vals[58])
        emitter.order_sensitive = float(vals[63])
        emitter.stqr_eq_end_size = float(vals[64])
        emitter.start_eq_end_rad = float(vals[65])
        emitter.end_rgb_var_sync = float(vals[67])
        emitter.start_rgb_var_sync = float(vals[68])
        
        emitter.fade_in = float(vals[41])
        emitter.fade_in_range = float(vals[42])
        emitter.fade_out = float(vals[43])
        emitter.fade_out_range = float(vals[44])
        emitter.friction_p = float(vals[59])
        emitter.friction_p_range = float(vals[60])
        emitter.friction_s = float(vals[68])
        emitter.friction_s_range = float(vals[69])
        emitter.friction_r = float(vals[70])
        emitter.friction_r_range = float(vals[71])
        emitter.respawn = float(vals[61])
        emitter.respawn_range = float(vals[62])

        return emitter





    def get_property_list(self):
        vals = [0 for _ in range(72)]

        vals[0] = self.max_particles
        vals[1] = self.duration
        vals[2] = self.lifetime
        vals[3] = self.lifetime_range
        vals[4] = self.emission
        vals[5] = self.angle
        vals[6] = self.angle_range
        vals[7] = self.speed
        vals[8] = self.speed_range
        vals[9] = self.pos_var_x
        vals[10] = self.pos_var_y
        vals[11] = self.gravity_x
        vals[12] = self.gravity_y
        vals[13] = self.accel_rad
        vals[14] = self.accel_rad_range
        vals[15] = self.accel_tan
        vals[16] = self.accel_tan_range

        vals[45] = self.start_rad
        vals[46] = self.start_rad_range
        vals[47] = self.end_rad
        vals[48] = self.end_rad_range
        vals[49] = self.rot_sec
        vals[50] = self.rot_sec_range

        vals[51] = self.use_radius

        vals[17] = self.start_size
        vals[18] = self.start_size_range
        vals[29] = self.end_size
        vals[30] = self.end_size_range
        vals[19] = self.start_spin
        vals[20] = self.start_spin_range
        vals[31] = self.end_spin
        vals[32] = self.end_spin_range

        vals[21] = self.start_r
        vals[22] = self.start_r_range
        vals[23] = self.start_g
        vals[24] = self.start_g_range
        vals[25] = self.start_b
        vals[26] = self.start_b_range
        vals[27] = self.start_a
        vals[28] = self.start_a_range
        vals[33] = self.end_r
        vals[34] = self.end_r_range
        vals[35] = self.end_g
        vals[36] = self.end_g_range
        vals[37] = self.end_b
        vals[38] = self.end_b_range
        vals[39] = self.end_a
        vals[40] = self.end_a_range

        vals[52] = self.free_relative_grouped

        vals[53] = self.additive
        vals[54] = self.start_eq_end_spin
        vals[55] = self.start_rot_is_dir
        vals[56] = self.dynamic_rotation
        vals[58] = self.uniform_obj_color
        vals[63] = self.order_sensitive
        vals[64] = self.stqr_eq_end_size
        vals[65] = self.start_eq_end_rad
        vals[67] = self.end_rgb_var_sync
        vals[68] = self.start_rgb_var_sync
        
        vals[41] = self.fade_in
        vals[42] = self.fade_in_range
        vals[43] = self.fade_out
        vals[44] = self.fade_out_range
        vals[59] = self.friction_p
        vals[60] = self.friction_p_range
        vals[68] = self.friction_s
        vals[69] = self.friction_s_range
        vals[70] = self.friction_r
        vals[71] = self.friction_r_range
        vals[61] = self.respawn
        vals[62] = self.respawn_range

        return 'a'.join(map(str, vals))





        '''
        max_particles = 0
        duration = 1
        lifetime = 2
        lifetime_range = 3
        emission = 4
        angle = 5
        angle_range = 6
        speed = 7
        speed_range = 8
        pos_var_x = 9
        pos_var_y = 10
        gravity_x = 11
        gravity_y = 12
        accel_rad = 13
        accel_rad_range = 14
        accel_tan = 15
        accel_tan_range = 16

        start_rad = 45
        start_rad_range = 46
        end_rad = 47
        end_rad_range = 48
        rot_sec = 49
        rot_sec_range = 50

        use_radius = 51


        start_size = 17
        start_size_range = 18
        end_size = 29
        end_size_range = 30
        start_spin = 19
        start_spin_range = 20
        end_spin = 31
        end_spin_range = 32

        start_r = 21
        start_r_range = 22
        start_g = 23
        start_g_range = 24
        start_b = 25
        start_b_range = 26
        start_a = 27
        start_a_range = 28
        end_r = 33
        end_r_range = 34
        end_g = 35
        end_g_range = 36
        end_b = 37
        end_b_range = 38
        end_a = 39
        end_a_range = 40

        free_relative_grouped = 52

        additive = 53
        start_eq_end_spin = 54
        start_rot_is_dir = 55
        dynamic_rotation = 56
        uniform_obj_color = 58
        order_sensitive = 63
        stqr_eq_end_size = 64
        start_eq_end_rad = 65
        end_rgb_var_sync = 67
        start_rgb_var_sync = 68



        
        fade_in = 41
        fade_in_range = 42
        fade_out = 43
        fade_out_range = 44
        friction_p = 59
        friction_p_range = 60
        friction_s = 68
        friction_s_range = 69
        friction_r = 70
        friction_r_range = 71
        respawn = 61
        respawn_range = 62

        '''