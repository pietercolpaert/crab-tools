import math

class LambertEllipsoid:
    def __init__(self, semi_major_axis, flattening):
        self.semi_major_axis = semi_major_axis
        self.flattening = flattening
        self.eccentricity = math.sqrt(self.flattening * (2.0 - self.flattening))

class LambertProjection:
    def __init__(self, name, ellipsoid, standard_parallel_1, standard_parallel_2, latitude_origin, longitude_origin, x_origin, y_origin):
        self.name = name
        self.ellipsoid = ellipsoid
        self.standard_parallel_1 = standard_parallel_1
        #print 'self.standard_parallel_1:' + str(self.standard_parallel_1)
        self.standard_parallel_1_radians = (self.standard_parallel_1 / 180.0) * math.pi
        #print 'self.standard_parallel_1_radians:' + str(self.standard_parallel_1_radians)
        self.standard_parallel_2 = standard_parallel_2
        #print 'self.standard_parallel_2:' + str(self.standard_parallel_2)
        self.standard_parallel_2_radians = (self.standard_parallel_2 / 180.0) * math.pi
        #print 'self.standard_parallel_2_radians:' + str(self.standard_parallel_2_radians)
        self.latitude_origin = latitude_origin
        #print 'self.latitude_origin:' + str(self.latitude_origin)
        self.latitude_origin_radians = (self.latitude_origin / 180.0) * math.pi
        #print 'self.latitude_origin_radians:' + str(self.latitude_origin_radians)
        self.longitude_origin = longitude_origin
        #print 'self.longitude_origin:' + str(self.longitude_origin)
        self.longitude_origin_radians = (self.longitude_origin / 180.0) * math.pi
        #print 'self.longitude_origin_radians:' + str(self.longitude_origin_radians)
        self.x_origin = x_origin
        #print 'self.x_origin:' + str(self.x_origin)
        self.y_origin = y_origin
        #print 'self.y_origin:' + str(self.y_origin)

        self.m_1 = (math.cos(self.standard_parallel_1_radians) / math.sqrt((1.0 - self.ellipsoid.eccentricity * self.ellipsoid.eccentricity * math.pow(math.sin(self.standard_parallel_1_radians), 2.0))))
        #print 'self.m_1:' + str(self.m_1)
        self.m_2 = (math.cos(self.standard_parallel_2_radians) / math.sqrt((1.0 - self.ellipsoid.eccentricity * self.ellipsoid.eccentricity * math.pow(math.sin(self.standard_parallel_2_radians), 2.0))))
        #print 'self.m_2:' + str(self.m_2)

        self.t_0 = (math.tan(math.pi / 4.0 - self.latitude_origin_radians / 2.0) / math.pow(((1.0 - self.ellipsoid.eccentricity * math.sin(self.latitude_origin_radians)) / (1.0 + self.ellipsoid.eccentricity * math.sin(self.latitude_origin_radians))), self.ellipsoid.eccentricity / 2.0))
        #print 'self.t_0:' + str(self.t_0)

        self.t_1 = (math.tan(math.pi / 4.0 - self.standard_parallel_1_radians / 2.0) / math.pow(((1.0 - self.ellipsoid.eccentricity * math.sin(self.standard_parallel_1_radians)) / (1.0 + self.ellipsoid.eccentricity * math.sin(self.standard_parallel_1_radians))), self.ellipsoid.eccentricity / 2.0))
        #print 'self.t_1:' + str(self.t_1)
            
        self.t_2 = (math.tan(math.pi / 4.0 - self.standard_parallel_2_radians / 2.0) / math.pow(((1.0 - self.ellipsoid.eccentricity * math.sin(self.standard_parallel_2_radians)) / (1.0 + self.ellipsoid.eccentricity * math.sin(self.standard_parallel_2_radians))), self.ellipsoid.eccentricity / 2.0))
        #print 'self.t_2:' + str(self.t_2)
            
        self.n = ((math.log(self.m_1) - math.log(self.m_2)) / (math.log(self.t_1) - math.log(self.t_2)))
        #print 'self.n:' + str(self.n)
        
        self.g = self.m_1 / (self.n * math.pow(self.t_1, self.n))
        #print 'self.g:' + str(self.g)
            
        self.r_0 = ellipsoid.semi_major_axis * self.g * math.pow(math.fabs(self.t_0), self.n)
        #print 'self.r_0:' + str(self.r_0)

    def to_wgs84(self, x, y):
        r = (math.sqrt(math.pow(x - self.x_origin, 2.0) + math.pow((self.r_0 - (y - self.y_origin)), 2.0)))
        #print 'r:' + str(r)
        #print 'self.x_origin:' + str(self.x_origin)
        t = math.pow((r / (self.ellipsoid.semi_major_axis * self.g)), 1.0 / self.n)
        #print 't:' + str(t)
        #print 'self.ellipsoid.semi_major_axis:' + str(self.ellipsoid.semi_major_axis)
        #print 'self.g:' + str(self.g)
        #print 'self.n:' + str(self.n)
        phi = math.atan((x - self.x_origin) / (self.r_0 - (y - self.y_origin)))
        #print 'phi:' + str(phi)
        longitude = ((phi / self.n) + self.longitude_origin_radians)
        #print 'longitude:' + str(longitude)
        latitude = (math.pi / 2.0 - 2.0 * math.atan(t))
        #print 'latitude:' + str(latitude)
        
        e = self.ellipsoid.eccentricity
        #print 'e' + str(e)
            
        new_latitude = 0;
        while(new_latitude != latitude):
            #print new_latitude, latitude
            new_latitude = latitude
            latitude = (math.pi / 2.0 - 2.0 * math.atan(t * math.pow(((1.0 - e * math.sin(latitude)) / (1.0 + e * math.sin(latitude))), e / 2.0)))
        
        hayford = Hayford1924Ellipsoid()
        phi_72 = latitude
        lambda_72 = longitude
        h_72 = 100
            
        a_72 = hayford.semi_major_axis
        e_72 = hayford.eccentricity
        es_72 = e_72 * e_72
        #print 'es_72:' + str(es_72)
        
        sin_phi_72 = math.sin(phi_72)
        #print 'sin_phi_72:' + str(sin_phi_72)
        cos_phi_72 = math.cos(phi_72)
        #print 'cos_phi_72:' + str(cos_phi_72)
        sin_lambda_72 = math.sin(lambda_72)
        #print 'sin_lambda_72:' + str(sin_lambda_72)
        cos_lambda_72 = math.cos(lambda_72)
        #print 'cos_lambda_72:' + str(cos_lambda_72)
        v_72 = a_72 / math.sqrt(1.0 - (es_72 * sin_phi_72 * sin_phi_72))
        #print 'v_72:' + str(v_72)
        
        x_72 = (v_72 + h_72) * cos_phi_72 * cos_lambda_72
        #print 'x_72:' + str(x_72)
        y_72 = (v_72 + h_72) * cos_phi_72 * sin_lambda_72
        #print 'y_72:' + str(y_72)
        z_72 = ((1.0 - es_72) * v_72 + h_72) * sin_phi_72
        #print 'z_72:' + str(z_72)
        
                
        # translations.
        x_trans = 106.868628;
        y_trans = 52.297783;
        z_trans = 103.723893;
                
        x_89 = x_72 - x_trans;
        #print 'x_89:' + str(x_89)
        y_89 = y_72 + y_trans;
        #print 'y_89:' + str(y_89)
        z_89 = z_72 - z_trans;
        #print 'z_89:' + str(z_89)
                
        # rotations.
        x_angle_degree = 0.336570 / 3600.0
        x_angle = (x_angle_degree / 180.0) * math.pi
        sin_x_angle = math.sin(x_angle)
        cos_x_angle = math.cos(x_angle)
        y_angle_degree = -0.456955 / 3600.0
        y_angle = (y_angle_degree / 180.0) * math.pi
        sin_y_angle = math.sin(y_angle)
        cos_y_angle = math.cos(y_angle)
        z_angle_degree = 1.842183 / 3600.0
        z_angle = (z_angle_degree / 180.0) * math.pi
        sin_z_angle = math.sin(z_angle)
        cos_z_angle = math.cos(z_angle)
            
        # rotate around x.
        # x_89 = x_89;
        y_89 = y_89 * cos_x_angle - z_89 * sin_x_angle;
        z_89 = y_89 * sin_x_angle + z_89 * cos_x_angle;
        # rotate around y.
        x_89 = x_89 * cos_y_angle + z_89 * sin_y_angle;
        # y_89 = y_89;
        z_89 = x_89 * (-sin_y_angle) + z_89 * cos_y_angle;
        # rotate around Z.
        x_89 = x_89 * cos_z_angle - y_89 * sin_z_angle;
        y_89 = x_89 * sin_z_angle + y_89 * cos_z_angle;
        # z_89 = z_89;
        #print 'x_89:' + str(x_89)
        #print 'y_89:' + str(y_89)
        #print 'z_89:' + str(z_89)

        wgs1984 = Wgs1984Ellipsoid()
        e = wgs1984.eccentricity
        es = e * e
        ps = x_89 * x_89 + y_89 * y_89
        p = math.sqrt(ps)
            
        r = math.sqrt(ps + z_89 * z_89)
        
        f = wgs1984.flattening
        a = wgs1984.semi_major_axis
        
        u = math.atan((z_89 / p) * ((1.0 - f) + (es * a / r)))
        lambda1 = math.atan(y_89 / x_89)
        phi = math.atan((z_89 * (1.0 - f) + (es * a * math.pow(math.sin(u), 3))) / ((1.0 - f) * (p - (es * a * math.pow(math.cos(u), 3)))))
 
        longitude_84 = (lambda1 / math.pi) * 180.0
        latitude_84 = (phi / math.pi) * 180.0
            
        return [ latitude_84, longitude_84 ]

class Belgium1972LambertProjection(LambertProjection):
    def __init__(self):
        LambertProjection.__init__(self, 'Belgium 1972 Projection', Hayford1924Ellipsoid(), 49.833334,51.166667, 90, 4.367487, 150000.01256, 5400088.438)

class Hayford1924Ellipsoid(LambertEllipsoid):
    def __init__(self):
        LambertEllipsoid.__init__(self, 6378388.0, 1.0 / 297.0)

class Wgs1984Ellipsoid(LambertEllipsoid):
    def __init__(self):
        LambertEllipsoid.__init__(self, 6378137.0, 1 / 298.257223563)

