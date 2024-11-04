import pandas as pd
from spline_force_mag import FFT_Processor

sim4_status = True
sim5_status = True
sim6_status = True
sim7_status = True
sim8_status = True
sim9_status = True

if sim4_status is True:
    sim4_10000x = FFT_Processor(speed=9988, mag_path='Sim4\\10k_mag_x.tab', phase_path='Sim4\\10k_phase_x.tab', max_order=100, min_magnitude=1.0)
    sim4_10000y = FFT_Processor(speed=9988, mag_path='Sim4\\10k_mag_y.tab', phase_path='Sim4\\10k_phase_y.tab', max_order=100, min_magnitude=1.0)
    sim4_7500x = FFT_Processor(speed=7505, mag_path='Sim4\\7k5_mag_x.tab', phase_path='Sim4\\7k5_phase_x.tab', max_order=100, min_magnitude=1.0)
    sim4_7500y = FFT_Processor(speed=7505, mag_path='Sim4\\7k5_mag_y.tab', phase_path='Sim4\\7k5_phase_y.tab', max_order=100, min_magnitude=1.0)
    sim4_5000x = FFT_Processor(speed=5002, mag_path='Sim4\\5k_mag_x.tab', phase_path='Sim4\\5k_phase_x.tab', max_order=100, min_magnitude=1.0)
    sim4_5000y = FFT_Processor(speed=5002, mag_path='Sim4\\5k_mag_y.tab', phase_path='Sim4\\5k_phase_y.tab', max_order=100, min_magnitude=1.0)
    sim4_2000x = FFT_Processor(speed=2012, mag_path='Sim4\\2k_mag_x.tab', phase_path='Sim4\\2k_phase_x.tab', max_order=100, min_magnitude=1.0)
    sim4_2000y = FFT_Processor(speed=2012, mag_path='Sim4\\2k_mag_y.tab', phase_path='Sim4\\2k_phase_y.tab', max_order=100, min_magnitude=1.0)
    sim4_750x = FFT_Processor(speed=781, mag_path='Sim4\\750_mag_x.tab', phase_path='Sim4\\750_phase_x.tab', max_order=100, min_magnitude=1.0)
    sim4_750y = FFT_Processor(speed=781, mag_path='Sim4\\750_mag_y.tab', phase_path='Sim4\\750_phase_y.tab', max_order=100, min_magnitude=1.0)

    with pd.ExcelWriter('loads_1_sim4_sim7_depth.xlsx') as writer:
        sim4_10000x.data.to_excel(writer, sheet_name='int_10k_x', index=False)
        sim4_10000y.data.to_excel(writer, sheet_name='int_10k_y', index=False)
        sim4_7500x.data.to_excel(writer, sheet_name='int_7k5_x', index=False)
        sim4_7500y.data.to_excel(writer, sheet_name='int_7k5_y', index=False)
        sim4_5000x.data.to_excel(writer, sheet_name='int_5k_x', index=False)
        sim4_5000y.data.to_excel(writer, sheet_name='int_5k_y', index=False)
        sim4_2000x.data.to_excel(writer, sheet_name='int_2k_x', index=False)
        sim4_2000y.data.to_excel(writer, sheet_name='int_2k_y', index=False)
        sim4_750x.data.to_excel(writer, sheet_name='int_750_x', index=False)
        sim4_750y.data.to_excel(writer, sheet_name='int_750_y', index=False)

if sim5_status is True:
    sim5_10000x = FFT_Processor(speed=9993, mag_path='Sim5\\10k_mag_x.tab', phase_path='Sim5\\10k_phase_x.tab')
    sim5_10000y = FFT_Processor(speed=9993, mag_path='Sim5\\10k_mag_y.tab', phase_path='Sim5\\10k_phase_y.tab')
    sim5_7500x = FFT_Processor(speed=7498, mag_path='Sim5\\7k5_mag_x.tab', phase_path='Sim5\\7k5_phase_x.tab')
    sim5_7500y = FFT_Processor(speed=7498, mag_path='Sim5\\7k5_mag_y.tab', phase_path='Sim5\\7k5_phase_y.tab')
    sim5_5000x = FFT_Processor(speed=4998, mag_path='Sim5\\5k_mag_x.tab', phase_path='Sim5\\5k_phase_x.tab')
    sim5_5000y = FFT_Processor(speed=4998, mag_path='Sim5\\5k_mag_y.tab', phase_path='Sim5\\5k_phase_y.tab')
    sim5_2000x = FFT_Processor(speed=1984, mag_path='Sim5\\2k_mag_x.tab', phase_path='Sim5\\2k_phase_x.tab')
    sim5_2000y = FFT_Processor(speed=1984, mag_path='Sim5\\2k_mag_y.tab', phase_path='Sim5\\2k_phase_y.tab')
    sim5_500x = FFT_Processor(speed=631, mag_path='Sim5\\500_mag_x.tab', phase_path='Sim5\\500_phase_x.tab')
    sim5_500y = FFT_Processor(speed=631, mag_path='Sim5\\500_mag_y.tab', phase_path='Sim5\\500_phase_y.tab')

    with pd.ExcelWriter('loads_2_sim5_sim8.xlsx') as writer:
        sim5_10000x.data.to_excel(writer, sheet_name='int_10k_x', index=False)
        sim5_10000y.data.to_excel(writer, sheet_name='int_10k_y', index=False)
        sim5_7500x.data.to_excel(writer, sheet_name='int_7k5_x', index=False)
        sim5_7500y.data.to_excel(writer, sheet_name='int_7k5_y', index=False)
        sim5_5000x.data.to_excel(writer, sheet_name='int_5k_x', index=False)
        sim5_5000y.data.to_excel(writer, sheet_name='int_5k_y', index=False)
        sim5_2000x.data.to_excel(writer, sheet_name='int_2k_x', index=False)
        sim5_2000y.data.to_excel(writer, sheet_name='int_2k_y', index=False)
        sim5_500x.data.to_excel(writer, sheet_name='int_500_x', index=False)
        sim5_500y.data.to_excel(writer, sheet_name='int_500_y', index=False)

if sim6_status is True:
    sim6_4700x = FFT_Processor(speed=4676, mag_path='Sim6\\4k7_mag_x.tab', phase_path='Sim6\\4k7_phase_x.tab')
    sim6_4700y = FFT_Processor(speed=4676, mag_path='Sim6\\4k7_mag_y.tab', phase_path='Sim6\\4k7_phase_y.tab')
    sim6_3000x = FFT_Processor(speed=3001, mag_path='Sim6\\3k_mag_x.tab', phase_path='Sim6\\3k_phase_x.tab')
    sim6_3000y = FFT_Processor(speed=3001, mag_path='Sim6\\3k_mag_y.tab', phase_path='Sim6\\3k_phase_y.tab')
    sim6_1500x = FFT_Processor(speed=1505, mag_path='Sim6\\1k5_mag_x.tab', phase_path='Sim6\\1k5_phase_x.tab')
    sim6_1500y = FFT_Processor(speed=1505, mag_path='Sim6\\1k5_mag_y.tab', phase_path='Sim6\\1k5_phase_y.tab')
    sim6_750x = FFT_Processor(speed=759, mag_path='Sim6\\750_mag_x.tab', phase_path='Sim6\\750_phase_x.tab')
    sim6_750y = FFT_Processor(speed=759, mag_path='Sim6\\750_mag_y.tab', phase_path='Sim6\\750_phase_y.tab')

    with pd.ExcelWriter('loads_3_sim6_sim9.xlsx') as writer:
        sim6_4700x.data.to_excel(writer, sheet_name='int_4k7_x', index=False)
        sim6_4700y.data.to_excel(writer, sheet_name='int_4k7_y', index=False)
        sim6_3000x.data.to_excel(writer, sheet_name='int_3k_x', index=False)
        sim6_3000y.data.to_excel(writer, sheet_name='int_3k_y', index=False)
        sim6_1500x.data.to_excel(writer, sheet_name='int_1k5_x', index=False)
        sim6_1500y.data.to_excel(writer, sheet_name='int_1k5_y', index=False)
        sim6_750x.data.to_excel(writer, sheet_name='int_750_x', index=False)
        sim6_750y.data.to_excel(writer, sheet_name='int_750_y', index=False)

if sim7_status is True:
    sim7_10000x = FFT_Processor(speed=9988, mag_path='Sim7\\10k_mag_x.tab', phase_path='Sim7\\10k_phase_x.tab')
    sim7_10000y = FFT_Processor(speed=9988, mag_path='Sim7\\10k_mag_y.tab', phase_path='Sim7\\10k_phase_y.tab')
    sim7_7500x = FFT_Processor(speed=7505, mag_path='Sim7\\7k5_mag_x.tab', phase_path='Sim7\\7k5_phase_x.tab')
    sim7_7500y = FFT_Processor(speed=7505, mag_path='Sim7\\7k5_mag_y.tab', phase_path='Sim7\\7k5_phase_y.tab')
    sim7_5000x = FFT_Processor(speed=5002, mag_path='Sim7\\5k_mag_x.tab', phase_path='Sim7\\5k_phase_x.tab')
    sim7_5000y = FFT_Processor(speed=5002, mag_path='Sim7\\5k_mag_y.tab', phase_path='Sim7\\5k_phase_y.tab')
    sim7_2000x = FFT_Processor(speed=2012, mag_path='Sim7\\2k_mag_x.tab', phase_path='Sim7\\2k_phase_x.tab')
    sim7_2000y = FFT_Processor(speed=2012, mag_path='Sim7\\2k_mag_y.tab', phase_path='Sim7\\2k_phase_y.tab')
    sim7_750x = FFT_Processor(speed=781, mag_path='Sim7\\750_mag_x.tab', phase_path='Sim7\\750_phase_x.tab')
    sim7_750y = FFT_Processor(speed=781, mag_path='Sim7\\750_mag_y.tab', phase_path='Sim7\\750_phase_y.tab')

    with pd.ExcelWriter('loads_1_sim4_sim7.xlsx', mode='a') as writer:
        sim7_10000x.data.to_excel(writer, sheet_name='split_10k_x', index=False)
        sim7_10000y.data.to_excel(writer, sheet_name='split_10k_y', index=False)
        sim7_7500x.data.to_excel(writer, sheet_name='split_7k5_x', index=False)
        sim7_7500y.data.to_excel(writer, sheet_name='split_7k5_y', index=False)
        sim7_5000x.data.to_excel(writer, sheet_name='split_5k_x', index=False)
        sim7_5000y.data.to_excel(writer, sheet_name='split_5k_y', index=False)
        sim7_2000x.data.to_excel(writer, sheet_name='split_2k_x', index=False)
        sim7_2000y.data.to_excel(writer, sheet_name='split_2k_y', index=False)
        sim7_750x.data.to_excel(writer, sheet_name='split_750_x', index=False)
        sim7_750y.data.to_excel(writer, sheet_name='split_750_y', index=False)

if sim8_status is True:
    sim8_10000x = FFT_Processor(speed=9993, mag_path='Sim8\\10k_mag_x.tab', phase_path='Sim8\\10k_phase_x.tab')
    sim8_10000y = FFT_Processor(speed=9993, mag_path='Sim8\\10k_mag_y.tab', phase_path='Sim8\\10k_phase_y.tab')
    sim8_7500x = FFT_Processor(speed=7498, mag_path='Sim8\\7k5_mag_x.tab', phase_path='Sim8\\7k5_phase_x.tab')
    sim8_7500y = FFT_Processor(speed=7498, mag_path='Sim8\\7k5_mag_y.tab', phase_path='Sim8\\7k5_phase_y.tab')
    sim8_5000x = FFT_Processor(speed=4998, mag_path='Sim8\\5k_mag_x.tab', phase_path='Sim8\\5k_phase_x.tab')
    sim8_5000y = FFT_Processor(speed=4998, mag_path='Sim8\\5k_mag_y.tab', phase_path='Sim8\\5k_phase_y.tab')
    sim8_2000x = FFT_Processor(speed=1984, mag_path='Sim8\\2k_mag_x.tab', phase_path='Sim8\\2k_phase_x.tab')
    sim8_2000y = FFT_Processor(speed=1984, mag_path='Sim8\\2k_mag_y.tab', phase_path='Sim8\\2k_phase_y.tab')
    sim8_500x = FFT_Processor(speed=631, mag_path='Sim8\\500_mag_x.tab', phase_path='Sim8\\500_phase_x.tab')
    sim8_500y = FFT_Processor(speed=631, mag_path='Sim8\\500_mag_y.tab', phase_path='Sim8\\500_phase_y.tab')

    with pd.ExcelWriter('loads_2_sim5_sim8.xlsx', mode='a') as writer:
        sim8_10000x.data.to_excel(writer, sheet_name='split_10k_x', index=False)
        sim8_10000y.data.to_excel(writer, sheet_name='split_10k_y', index=False)
        sim8_7500x.data.to_excel(writer, sheet_name='split_7k5_x', index=False)
        sim8_7500y.data.to_excel(writer, sheet_name='split_7k5_y', index=False)
        sim8_5000x.data.to_excel(writer, sheet_name='split_5k_x', index=False)
        sim8_5000y.data.to_excel(writer, sheet_name='split_5k_y', index=False)
        sim8_2000x.data.to_excel(writer, sheet_name='split_2k_x', index=False)
        sim8_2000y.data.to_excel(writer, sheet_name='split_2k_y', index=False)
        sim8_500x.data.to_excel(writer, sheet_name='split_500_x', index=False)
        sim8_500y.data.to_excel(writer, sheet_name='split_500_y', index=False)

if sim9_status is True:
    sim9_4700x = FFT_Processor(speed=4676, mag_path='Sim9\\4k7_mag_x.tab', phase_path='Sim9\\4k7_phase_x.tab')
    sim9_4700y = FFT_Processor(speed=4676, mag_path='Sim9\\4k7_mag_y.tab', phase_path='Sim9\\4k7_phase_y.tab')
    sim9_3000x = FFT_Processor(speed=3001, mag_path='Sim9\\3k_mag_x.tab', phase_path='Sim9\\3k_phase_x.tab')
    sim9_3000y = FFT_Processor(speed=3001, mag_path='Sim9\\3k_mag_y.tab', phase_path='Sim9\\3k_phase_y.tab')
    sim9_1500x = FFT_Processor(speed=1505, mag_path='Sim9\\1k5_mag_x.tab', phase_path='Sim9\\1k5_phase_x.tab')
    sim9_1500y = FFT_Processor(speed=1505, mag_path='Sim9\\1k5_mag_y.tab', phase_path='Sim9\\1k5_phase_y.tab')
    sim9_750x = FFT_Processor(speed=759, mag_path='Sim9\\750_mag_x.tab', phase_path='Sim9\\750_phase_x.tab')
    sim9_750y = FFT_Processor(speed=759, mag_path='Sim9\\750_mag_y.tab', phase_path='Sim9\\750_phase_y.tab')

    with pd.ExcelWriter('loads_3_sim6_sim9.xlsx', mode='a') as writer:
        sim9_4700x.data.to_excel(writer, sheet_name='split_4k7_x', index=False)
        sim9_4700y.data.to_excel(writer, sheet_name='split_4k7_y', index=False)
        sim9_3000x.data.to_excel(writer, sheet_name='split_3k_x', index=False)
        sim9_3000y.data.to_excel(writer, sheet_name='split_3k_y', index=False)
        sim9_1500x.data.to_excel(writer, sheet_name='split_1k5_x', index=False)
        sim9_1500y.data.to_excel(writer, sheet_name='split_1k5_y', index=False)
        sim9_750x.data.to_excel(writer, sheet_name='split_750_x', index=False)
        sim9_750y.data.to_excel(writer, sheet_name='split_750_y', index=False)