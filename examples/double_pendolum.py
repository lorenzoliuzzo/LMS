from src.surfaces import parametrization, double_pendolum
from src.potentials import potential_energy, gravity
from src.lagrangian import evolve_lagrangian
from src.plotting import animate_3D_trajectory 

import jax
from jax import numpy as jnp
import numpy as np
import os
import time


# setting the randomness
seed = np.random.randint(0, 1000)
key = jax.random.PRNGKey(seed)

# setting the data directory for saving the trajectory
data_dir = 'data/dp/' + str(seed)
os.makedirs(data_dir, exist_ok=True)

# setting the initial conditions
nbodies = ndim = 2
mass = jax.random.uniform(key, (nbodies,))
q = jax.random.uniform(key, (nbodies, ndim))
q_t = jax.random.uniform(key, (nbodies, ndim))

# creating the constraint with parametrization
constraint = parametrization(double_pendolum, l1=np.random.random(), l2=np.random.random())

# creating the gravity with potential_energy
g_pot = potential_energy(gravity, g=9.81)   

# setting the time evolution parameters
tmax = 20.
npoints = 500
tspan = jnp.linspace(0., tmax, npoints)

# evolving the lagrangian
start = time.time()
positions, velocities = evolve_lagrangian(tspan, q, q_t, mass, potentials=[g_pot], constraint=constraint)
end = time.time()
print(f"Evolution finished in {end - start} s")

# save data
jnp.save(os.path.join(data_dir, 't.npy'), tspan)
jnp.save(os.path.join(data_dir, 'q.npy'), positions)
jnp.save(os.path.join(data_dir, 'q_t.npy'), velocities)

# animate the trajectory
animate_3D_trajectory(tspan, positions, constraint)