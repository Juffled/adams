from sound_power_calculator import SoundPowerCalculator
from sound_power_processing import SoundPowerProcessor


# Get your FFT data into Python, read the tables and calculate the sound power for different sets of test data,

# e.g.

# test data and test data 1 --> Bearing 1 and Bearing 2 at same speed and torque, so sound power gets added up

# test data 2 and test data 3 --> bearing 1 and bearing 2 at a higher speed and different torques,

# We would expect to have 3 sets of results from this, test data 1 and 2 are from the same loadcase and would combine
# for a total acoustic power value, and test data 3 and 4 would stay separate due to them being different load cases,
# this is all automatically identified by the code based upon speed and torque values, so different gearbox layouts need
# different script files to run the code or it will add gearbox A loadcase 1 to gearbox B loadcase 1


test_data_1 = SoundPowerCalculator(speed_rpm=2012.0, torque_nm=20.0,
                                  f_mag_path='test_data\\2k_mag_x.tab', f_phase_path='test_data\\2k_phase_x.tab',
                                  v_mag_path='test_data\\2k_mag_y.tab', v_phase_path='test_data\\2k_phase_y.tab')

test_data_2 = SoundPowerCalculator(speed_rpm=2012.0, torque_nm=20.0,
                                   f_mag_path='test_data\\2k_mag_x1.tab', f_phase_path='test_data\\2k_phase_x1.tab',
                                   v_mag_path='test_data\\2k_mag_y1.tab', v_phase_path='test_data\\2k_phase_y1.tab')

test_data_3 = SoundPowerCalculator(speed_rpm=5002.0, torque_nm=20.0,
                                   f_mag_path='test_data\\5k_mag_x.tab', f_phase_path='test_data\\5k_phase_x.tab',
                                   v_mag_path='test_data\\5k_mag_y.tab', v_phase_path='test_data\\5k_phase_y.tab')

test_data_4 = SoundPowerCalculator(speed_rpm=5002.0, torque_nm=40.0,
                                   f_mag_path='test_data\\5k_mag_x1.tab', f_phase_path='test_data\\5k_phase_x1.tab',
                                   v_mag_path='test_data\\5k_mag_y1.tab', v_phase_path='test_data\\5k_phase_y1.tab')

# Create your Sound Power processor and it will automatically process the data basd upon frequency, torque and speed
my_sound_power = SoundPowerProcessor(power_data_list=[test_data_1.data, test_data_2.data, test_data_3.data, test_data_4.data])

# Plot Results
# All the data is now in the processor, so you need to tell it what to plot and what to use for the x axis, speed or torque?
my_sound_power.plot(speed_rpm=2012, torque_nm=20, frequency_limit=2000, x_speed=True, title='Total Acoustic Power [W]')
my_sound_power.plot(torque_nm=20, frequency_limit=2000, x_speed=True, title='Acoustic Power [W] at Different Speeds')
my_sound_power.plot(speed_rpm=5002, frequency_limit=2000, x_torque=True, title='Acoustic Power [W] at Different Torque')
