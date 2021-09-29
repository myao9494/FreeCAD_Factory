# -*- coding: utf-8 -*-
import FreeCAD as App
import WF
from WF_print import printError_msg, print_msg
if App.GuiUp:
    import FreeCADGui as Gui


def init_min_max():
    """ Return min and max values from System.
    min_val, max_val = init_min_max
    """
    import sys
    if sys.version < '3.0.0':
        max_val = sys.maxsize
        min_val = -sys.maxsize - 1
    # for python 3.0 use sys.maxsize
    else:
        max_val = sys.maxsize
        min_val = -sys.maxsize - 1
    return min_val, max_val


def isColinearVectors(vect_a, vect_b, vect_c):
    """ Return true if the 3 points are aligned.
    """
    Vector_1 = vect_b - vect_a
    Vector_2 = vect_c - vect_b
    Vector_3 = Vector_1.cross(Vector_2)
    m_tolerance = WF.tolerance()

    if abs(Vector_3.x) <= m_tolerance and abs(
            Vector_3.y) <= m_tolerance and abs(Vector_3.z) <= m_tolerance:
        return True

    return False


def isEqualVectors(vect_a, vect_b):
    """ Return true if the 2 points are equal.
    """
    Vector = vect_b - vect_a
    m_tolerance = WF.tolerance()
    if abs(Vector.x) <= m_tolerance and abs(
            Vector.y) <= m_tolerance and abs(Vector.z) <= m_tolerance:
        return True

    return False


def centerLinePoint(edge):
    """ Return the center point of the Line.
    """
    Vector_A = edge.Vertexes[0].Point
    Vector_B = edge.Vertexes[-1].Point
    Vector_AB = Vector_B + Vector_A

    return Vector_AB.multiply(0.5)


def alongTwoPointsPoint(vect_a, vect_b, index, number):
    """ Return the point at index/number of the Line defined by vect_a and vect_b.
    1/2 means middle of the line.
    1/3 means one third of the line...
    """
    Vector_A = vect_a
    Vector_B = vect_b
    distance = Vector_B.sub(Vector_A).Length / 2

    if number != 0:
        distance = index * (Vector_B.sub(Vector_A).Length / number)
    Vector_A = Vector_A.add(Vector_B.sub(
        Vector_A).normalize().multiply(distance))

    return Vector_A


def alongLinePoint(edge, index, number):
    """ Return the point at index/number of the Line.
    1/2 means middle of the line.
    1/3 means one third of the line...
    """
    Vector_A = edge.Vertexes[0].Point
    Vector_B = edge.Vertexes[-1].Point
    if isEqualVectors(Vector_A, Vector_B):
        return None
    distance = Vector_B.sub(Vector_A).Length / 2

    if number != 0:
        distance = index * (edge.Length / number)
    Vector_A = Vector_A.add(Vector_B.sub(
        Vector_A).normalize().multiply(distance))

    return Vector_A


def coordVectorPoint(vertex):
    """ Return the coordinates (x,y,z) of selected Vector.
    """
    m_coord = (0.0, 0.0, 0.0)
    m_vert = vertex

    if vertex is None:
        print_msg("ERROR : vertex == None, leaving coordVectorPoint()")
        return m_coord

    return (m_vert.x, m_vert.y, m_vert.z)


def meanVectorsPoint(vertexes):
    """ Return the mean point of all selected Vectors.
    """
    Vector_mean = App.Vector(0.0, 0.0, 0.0)
    m_vertx = vertexes
    m_num = len(m_vertx)
    if m_num == 0:
        return None

    if vertexes is None:
        print_msg("ERROR : vertexes == None, leaving meanVectorsPoint()")
        return Vector_mean
    if m_num < 1:
        print_msg("ERROR : len(vertexes) < 1 , meanVectorsPoint()")
        return Vector_mean
    m_list = []
    for m_vert in m_vertx:
        m_list.append(m_vert.x)
        m_list.append(m_vert.y)
        m_list.append(m_vert.z)

    import numpy
    m_vect = numpy.array(m_list)
    m_vect_re = m_vect.reshape(m_num, 3)
    vect_c = sum(m_vect_re, 0) / m_num

    Vector_mean = App.Vector(vect_c[0], vect_c[1], vect_c[2])

    return Vector_mean


def minMaxVectorsLimits(vertexes):
    """ Return the min and max limits along the 3 Axis for all selected Vectors.
    """
    xmax = xmin = ymax = ymin = zmax = zmin = 0
    m_vertx = vertexes
    m_num = len(m_vertx)

    if vertexes is None:
        print_msg("ERROR : vertexes == None, leaving minMaxVectorsLimits()")
        return xmax, xmin, ymax, ymin, zmax, zmin

    if m_num < 1:
        print_msg("ERROR : len(vertexes) < 1 , leaving minMaxVectorsLimits()")
        return xmax, xmin, ymax, ymin, zmax, zmin

    min_val, max_val = init_min_max()
    xmin = ymin = zmin = max_val
    xmax = ymax = zmax = min_val

    for m_vert in m_vertx:
        xmax = max(xmax, m_vert.x)
        xmin = min(xmin, m_vert.x)
        ymax = max(ymax, m_vert.y)
        ymin = min(ymin, m_vert.y)
        zmax = max(zmax, m_vert.z)
        zmin = min(zmin, m_vert.z)

    return xmax, xmin, ymax, ymin, zmax, zmin


def intersecLinePlane(vect_a, vect_b, Plane_Normal, Plane_Point):
    """ Return the intersection between the Line L defined by vect_a and vect_b
    and the Plane defined by Plane_Normal and Plane_Point.
    """
    # Plane Equation is eq(0) P(x, y, z):
    # a * x + b * y + c * z + d = 0
    # where Normal to P is  N(a, b, c)
    N = Plane_Normal

    # if N == App.Vector(0.0, 0.0, 0.0):
    #    return None
    a, b, c = N.x, N.y, N.z
    # print("a = " + str(a) + " b = " + str(b) + " c = " + str(c))

    # p1(px,py,pz) belongs to the plane P, so
    # a * px + b * py + c * pz + d = 0 and
    # d = -(a * px + b * py + c * pz)
    p1 = Plane_Point
    d = -((a * p1.x) + (b * p1.y) + (c * p1.z))
    # print("d = "+ str(d))

    # L is the line defined by 2 points vect_a(ax, ay, az) and vect_b(bx, by, bz), and
    # may be also defined as the line crossing vect_a(ax, ay, az) and along
    # the direction AB = U(bx-ax, by-ay, bz-az)
    # If U(ux, uy, uz) = U(bx-ax, by-ay, bz-az) the Line L is the set of
    # points M as defined by eq(1):
    # Vector(MA) = k * Vector(U)
    # with k Real
    if isEqualVectors(vect_a, vect_b):
        print_msg("ERROR : The 2 given points are equals !")
        return None
    ax, ay, az = vect_a.x, vect_a.y, vect_a.z
    bx, by, bz = vect_b.x, vect_b.y, B.z
    ux, uy, uz = bx - ax, by - ay, bz - az
    U = App.Vector(ux, uy, uz)

    # We consider Dot product between U and N
    # 1> U.N = 0
    # print("U.dot(N) =" + str(U.dot(N)))

    if U.dot(N) == 0.0:
        # if vect_a belongs to P : the full Line L is included in the Plane
        if (a * ax) + (b * ay) + (c * az) + d == 0.0:
            print_msg(
                "WARNING : The full Line is included in the Plane, returning first Point !")
            return vect_a
        # if not the Plane and line are parallel without intersection
        else:
            print_msg(
                "ERROR : The Plane and the line are parallel without intersection !")
            return None
    # 2> U.N != 0
    else:
        # We look for T(tx, ty, tz) on the Line L
        # eq(1) in parametric form; k exists and follows eq(2):
        # tx = ax + k * ux
        # ty = ay + k * uy
        # tz = az + k * uz
        # and T(tx, ty, tz) on the plane too so eq(1) is
        # a * tx + b * ty + c * tz + d = 0
        # by pasting the tx, ty and tz expressions into eq(1) we have a first
        # deg equation with one unknown 'k':
        # a * (ax + k * ux) + b * (ay + k * uy) + c * (az + k * uz) + d = 0
        # so
        # a * ax + a * k * ux + b * ay + b * k * uy + c * az + c * k * uz + d = 0
        # k * ( a * ux + b * uy  c *uz ) + a * ax + b * ay + c * az  + d = 0
        # k = -1 * (a * ax + b * ay + c * az  + d) / ( a * ux + b * uy + c *uz )
        if (a * ux + b * uy + c * uz) == 0.0:
            print_msg("ERROR : a * ux + b * uy + c *uz == 0.0 !")
            return None

        k = -1 * (a * ax + b * ay + c * az + d) / (a * ux + b * uy + c * uz)
        tx = ax + k * ux
        ty = ay + k * uy
        tz = az + k * uz
        # print("tx =" + str(tx) + " ty=" + str(ty) + " tz=" + str(tz))
        T = App.Vector(tx, ty, tz)

        return T


def intersectPerpendicularLine(vect_a, vect_b, point_c,):
    """ Return the projection of point_c onto line [vect_a,vect_b].

    Calculate the intersection between the Line L defined by vect_a and vect_b
    and the Line perpendicular crossing the point_c.
    This is also the projection of point_c onto the Line L.

    Return also the distance between point_cC and the the projection.
    Return also the symmetric point of point_c versus the Line.

    RETURN:
    -------
    T, distance, Tprime
    PARAMETERS:
    -----------
    vect_a    : (Vector, Mandatory)
    vect_b    : (Vector, Mandatory)
    point_c    : (Vector, Mandatory)
>>>>>>> Build useful functions
    """
    import math
    # L is the line defined by 2 points vect_a(ax, ay, az) and vect_b(bx, by, bz), and
    # may be also defined as the line crossing vect_a(ax, ay, az) and along the
    # direction AB = U(bx-ax, by-ay, bz-az)
    # If U(ux, uy, uz) = U(bx-ax, by-ay, bz-az) the Line L is the set of
    # points M as defined by eq(1):
    # Vector(MA) = k * Vector(U)
    # with k Real
    if vect_a == vect_b:
        return None
    ax, ay, az = vect_a.x, vect_a.y, vect_a.z
    bx, by, bz = vect_b.x, vect_b.y, vect_b.z
    cx, cy, cz = point_c.x, point_c.y, point_c.z
    ux, uy, uz = bx - ax, by - ay, bz - az
    # U = App.Vector(ux, uy, uz)
    # We look for T(tx, ty, tz) on the Line L
    # eq(1) in parametric form; k exists and follows eq(2):
    # tx = ax + k * ux
    # ty = ay + k * uy
    # tz = az + k * uz

    # and vector V(vx, vy, vz) defined by point C and point T
    # vx, vy, vz = tx - cx, ty - cy, tz - cz
    # V must be perpendicular to the Line L
    # We consider Dot product between U and V and give us eq(3)
    # U.V = 0
    # so ux * vx + uy * vy + uz * vz = 0
    # ux * (tx - cx) + uy * (ty - cy) + uz * (tz - cz) = 0
    # ux * (ax + k * ux  - cx) + uy * (ay + k * uy - cy) + uz * (az + k * uz  - cz) = 0
    # ux*ax + ux*(k*ux) - ux*cx + uy*ay + uy*(k*uy) - uy*cy +  uz*az +
    # uz*(k*uz) - uz*cz = 0
    if (ux * ux + uy * uy + uz * uz) == 0.0:
        return None
    k = (ux * cx + uy * cy + uz * cz - ux * ax - uy *
         ay - uz * az) / (ux * ux + uy * uy + uz * uz)
    tx = ax + k * ux
    ty = ay + k * uy
    tz = az + k * uz
    T = App.Vector(tx, ty, tz)
    vx, vy, vz = tx - cx, ty - cy, tz - cz
    V = App.Vector(vx, vy, vz)
    distance = math.sqrt(V.dot(V))
    Tprime = T + V

    return T, distance, Tprime


def printPoint(point, msg=""):
    """ Print x,y and z of a point:vector.
    """
    if point.__class__.__name__ != "Vector":
        print_msg("Not a Vector to print !")
        return

    print_msg(str(msg) + " " +
              "x =" + str(point.x) + ", "
              "y =" + str(point.y) + ", "
              "z =" + str(point.z))
    return


def propertiesPoint(Point_User_Name,
                    color=(1.00, 0.67, 0.00)):
    """ Define the properties of a Work feature Point.
    PointColor
    PointSize
    Transparency
    """
    try:
        if isinstance(color, tuple):
            Gui.ActiveDocument.getObject(Point_User_Name).PointColor = color
    except Exception as err:
        printError_msg(err.args[0], title="propertiesPoint")
        print_msg("Not able to set PointColor !")
        print_msg("Color : " + str(color) + " !")
    try:
        Gui.ActiveDocument.getObject(
            Point_User_Name).PointSize = WF.pointSize()

    except Exception as err:
        printError_msg(err.args[0], title="propertiesPoint")
        print_msg("Not able to set PointSize !")
    try:
        Gui.ActiveDocument.getObject(Point_User_Name).Transparency = 0
    except Exception as err:
        printError_msg(err.args[0], title="propertiesPoint")
        print_msg("Not able to set Transparency !")

    return


def propertiesLine(Line_User_Name,
                   color=(1.00, 0.67, 0.00)):
    """ Define the properties of a Work feature Line.
    PointColor
    LineColor
    LineWidth
    PointSize
    Transparency
    """
    try:
        if isinstance(color, tuple):
            Gui.ActiveDocument.getObject(Line_User_Name).PointColor = color
    except Exception as err:
        printError_msg(err.args[0], title="propertiesLine")
        print_msg("Not able to set PointColor !")
        print_msg("Color : " + str(color) + " !")
    try:
        if isinstance(color, tuple):
            Gui.ActiveDocument.getObject(Line_User_Name).LineColor = color
    except Exception as err:
        printError_msg(err.args[0], title="propertiesLine")
        print_msg("Not able to set LineColor !")
        print_msg("Color : " + str(color) + " !")
    try:
        Gui.ActiveDocument.getObject(
            Line_User_Name).LineWidth = WF.lineThickness()
    except Exception as err:
        printError_msg(err.args[0], title="propertiesLine")
        print_msg("Not able to set LineWidth !")
    try:
        Gui.ActiveDocument.getObject(
            Line_User_Name).PointSize = WF.linePointSize()
    except Exception as err:
        printError_msg(err.args[0], title="propertiesLine")
        print_msg("Not able to set PointSize !")
    try:
        Gui.ActiveDocument.getObject(Line_User_Name).Transparency = 0
    except Exception as err:
        printError_msg(err.args[0], title="propertiesLine")
        print_msg("Not able to set Transparency !")

    return


def propertiesPlane(Plane_User_Name,
                    color=(1.00, 0.67, 0.00),
                    s_color=(0.00, 0.33, 1.00)):
    """ Define the properties of a Work feature Plane.
    PointColor
    LineColor
    ShapeColor
    Transparency
    """
    try:
        if isinstance(color, tuple):
            Gui.ActiveDocument.getObject(Plane_User_Name).PointColor = color
    except Exception as err:
        printError_msg(err.args[0], title="propertiesPlane")
        print_msg("Not able to set PointColor !")
    try:
        if isinstance(color, tuple):
            Gui.ActiveDocument.getObject(Plane_User_Name).LineColor = color
    except Exception as err:
        printError_msg(err.args[0], title="propertiesPlane")
        print_msg("Not able to set LineColor !")
    try:
        if isinstance(s_color, tuple):
            Gui.ActiveDocument.getObject(Plane_User_Name).ShapeColor = s_color
    except Exception as err:
        printError_msg(err.args[0], title="propertiesPlane")
        print_msg("Not able to set ShapeColor !")
    try:
        Gui.ActiveDocument.getObject(Plane_User_Name).Transparency = 75
    except Exception as err:
        printError_msg(err.args[0], title="propertiesPlane")
        print_msg("Not able to set Transparency !")

    return
