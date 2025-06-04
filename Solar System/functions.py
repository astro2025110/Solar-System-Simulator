import numpy as np
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter
from mpl_toolkits import mplot3d
import data
import random

# Insert all constants from NASA Horizons data here in a dictionary
const = {
    "G": 66364.27, # m^3 / kg*yr^2
    "AU": 149597870700.0, #m
}

# Universal Gravitational Force
def F_gravity(ri=1, rj=1, mi=1, mj=1):
    k = const["G"] * mi * mj
    r = rj - ri
    rlength = np.sqrt(np.sum(r*r))
    return k*(1/rlength**3) * r

# Net gravity
def a_net(n, ri=1, rj=1, mi=1, mj=1):
    F = []
    a_net = []
    if n > 2:
        for i in range(n-1):
            #print(f"i={i}")
            Fnet = 0
            for j in range(n-1):
                if np.array_equal(ri[i], rj[j]):
                    #print(f"j={j}, ri={ri[i]}, rj={rj[j]} Fnet={Fnet}")
                    continue
                else:
                    k = const["G"] * mi[i] * mj[j]
                    r = rj[j] - ri[i]
                    rlength = np.sqrt(np.sum(r*r))
                    Fnet += k*(1/rlength**3) * r
                    #print(f"j={j}, ri={ri[i]}, rj={rj[j]} Fnet={Fnet}")
            F.append(Fnet)
            a_net.append(Fnet/mi[i])
    else:
        k = const["G"] * mi * mj
        r = rj - ri
        rlength = np.sqrt(np.sum(r*r))
        a_net = (k*(1/rlength**3)*r)/mi
    return a_net
 
# Velocity verlet integrator
def integrate(n=1, ri=1, rj=1, mi=1, mj=1, vi=1, dt=1, t=0, t_max=1):
    '''
    This function computes r(t) and v(t) given initial conditions r(0), v(0)
    '''
    if n <= 2:
        r = np.zeros(3)
        v = np.zeros(3)
        a = np.zeros(3)
    else:
        r = np.zeros((n-1, 3))  # (x, y, z)
        v = np.zeros((n-1, 3))  # (vx, vy, vz)
        a = np.zeros((n-1, 3)) # (ax, ay, az)
    
    #initial conditions
    
    #ri_0 = ri
    vi_0 = vi
    rj_0 = rj
    r[:] = ri
    v[:] = vi_0

    r_values = [ri]
    
    v_values = [vi_0]    
    t_values = [t]
    
    N_steps = int(t_max / dt)
    a = a_net(n=n, ri=ri, rj=rj_0, mi=mi, mj=mj)
    a_vals = [a]

    for i in range(N_steps):
        t += dt
    
        # velocity Verlet
        if n <= 2:
            v_half = v + 0.5*dt*a    # half-step velocity
            ri_new = r + dt*v_half
            a_new = a_net(n=n, ri=ri_new, rj=rj_0, mi=mi, mj=mj)
            vi_new = v_half + 0.5*dt*a_new
        else:
            v_half = np.zeros((n-1, 3))
            ri_new = np.zeros((n-1, 3))
            vi_new = np.zeros((n-1, 3))
            rj_new = np.zeros((n, 3))
            for i in range(len(a)):
                v_half[i] = v[i] + 0.5*dt*a[i]    # half-step velocity
                ri_new[i] = r[i] + dt*v_half[i]
                rj_new[i+1] = ri_new[i]    
            #rj_new.append(ri_new)
            a_new = a_net(n=n, ri=ri_new, rj=rj_new, mi=mi, mj=mj)
            for i in range(len(a_new)):
                vi_new[i] = v_half[i] + 0.5*dt*a_new[i]
    
        r_values.append(ri_new)
        v_values.append(vi_new)
        t_values.append(t)
        a_vals.append(a_new)

        r[:] = ri_new
        v[:] = vi_new
        a = a_new    # important: use force/acceleration for next step!

        # turn lists of results into arrays for easier processing
    r_values = np.array(r_values)
    v_values = np.array(v_values)
    t_values = np.array(t_values)
        
    
    return r_values, v_values, t_values

class Positions:
    # Class variable
    species = "body"

    # Constructor
    def __init__(self, name, r):  #As much data as you want!
        # Instance variables
        self.name = name
        self.r = r/const["AU"]
        self.x = self.r[:, 0]
        self.y = self.r[:, 1]
        self.z = self.r[:, 2]
        if name == "Sun":
            self.color = "yellow"
        else:
            self.color = random_color_gen()

def calculate_orbits(t, t_max, dt):
    ri = []
    vi = []
    mi = []
    # Take a list of planets/asteroids as input
    objects = list(input("Enter a list of planets/asteroids from the data: ").split(","))
    n = len(objects)+1
    print(n)
    i = 0
    for name in range(n-1):
        print(i)
        objects[name] = getattr(data, objects[name])
        #objects[name] = data.objects[name] #converts list of strings to variables that are defined as objects in Bodies class from data
        ri.append(objects[name].position)
        vi.append(objects[name].velocity)
        mi.append(objects[name].mass)
        i += 1
    ri = np.array(ri)
    mi = np.array(mi)
    vi = np.array(vi)
    
    stars = list(input("Enter the star: ").split(","))
    stars[0] = getattr(data, stars[0])
    if n > 2:
        rj = ri.tolist()
        print(rj)
        rj = rj.append(stars[0].position.tolist())
        #rj = np.array(rj)
        print(rj)
        mj = mi.tolist()
        print(mj)
        mj = mj.append(stars[0].mass.tolist())
        #mj = np.array(mj)
        print(mj)
    else:
        rj = stars[0].position
        mj = stars[0].mass
        print(rj)
        print(mj)

    r, v, t = integrate(n=n,ri=ri,vi=vi,mi=mi,rj=rj,mj=mj,dt=dt,t=t,t_max=t_max)
    pos = []
    for i in range(n-1):
        obj = Positions("planet", r[:,i,:])
        pos.append(obj)
    return pos, t



#Function for 2D plot
def plot_2D(t, t_max, dt):
    pos, t = calculate_orbits(t, t_max, dt)
    plt.figure(figsize=(8, 6))
    plt.plot(pos[0].x, pos[0].y)
    #for obj in pos:
        #plt.plot(obj.x, obj.y, label=obj.name)
    
    plt.title(f"Solar System Simulation for {t_max} years")
    plt.xlabel("X (AU)")
    plt.ylabel("Y (AU)")
    #plt.savefig("Earth-Sun System(1 year)")
    plt.show()
    plt.close()

    return

#Function for 3D plot
def random_color_gen():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)

def plot_3D(n, planets):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax = plt.axes(projection='3d')
    for i in range(n-1):
        ax.plot3D(planets[i].x, planets[i].y, planets[i].z, label=planets[i].name)
        #ax.scatter(planets[i].x[5], planets[i].y[5], planets[i].z[5], s=100, marker='o')
    #plt.scatter(0, 0, s=100, color='yellow', marker='o') # Adds Sun on the curve
    ax.set_xlabel('X (AU)')
    ax.set_ylabel('Y (AU)')
    ax.set_zlabel('Z (AU)')
    plt.show()
    plt.close()