"""Helper functions for server.py for Grab Back"""

import numpy as np
from sqlalchemy import func

from model import Location, CitizenGroup, Zipcode, connect_to_db, db

def format_manager_data(year):
    year = int(year)

    has_pop = db.session.query(
        CitizenGroup.location_id,
        CitizenGroup.population, CitizenGroup.year).filter(CitizenGroup.population.isnot(None))

    # MANAGERS
    f_data = has_pop.filter_by(female=True, manager=True, year=year).all()
    f_data_np = np.array(f_data)
    f_pop = f_data_np[:, 1]
    m_data = has_pop.filter_by(female=False, manager=True, year=year).all()
    m_data_np = np.array(m_data)
    m_pop = m_data_np[:, 1]
    total_pop = f_pop + m_pop

    final_data = np.column_stack((f_data_np[:, 0], (f_pop/total_pop)))
    final_data = final_data.tolist()

    data_dict = {}

    for i in range(len(final_data)):
        data_dict[int(final_data[i][0])] = final_data[i][1]

    return data_dict
