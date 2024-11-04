import xml.etree.ElementTree as etree
import time
import sys
import math
import os
#import Adams


# filename = 'boo_sin.res'
ns = "{http://www.mscsoftware.com/:xrf10}"

verbose = 0

def print_all_xml_tags(file_name):
    """
    Iterate through xml file
    :param file_name:
    :return:
    """

    for event, elem in etree.iterparse(file_name):
        print(event, elem)

    return


def print_stepmap(file_name):
    """
    Iterate through xml file
    :param file_name:
    :return:
    """

    stepmap_tag = ns + 'StepMap'

    for event, elem in etree.iterparse(file_name):
        # print event, elem

        if 'StepMap' in elem.tag:
            # Just processed stepmap, print it:
            print('------ Stepmap: --------')
            for e in elem.iter():
                print(e, e.get('name'))


def get_stepmap_dictionary(file_name):           ###
    """
    Create dictionary where keys=res name and
    values = index of component.
    res names must be full, like:
    time.time
    part_2_xform.fx
    part_3_xform.accy
    :param file_name:
    :return:
    """
    stepmap_tag = ns + 'StepMap'

    step_dict = {}

    for event, elem in etree.iterparse(file_name):
        # print event, elem

        if 'StepMap' in elem.tag:
            # Just processed stepmap, print it:
            # print('------ Stepmap: --------')

            ent_name = ''
            for e in elem.iter():
                if 'Entity' in e.tag:
                    # found a new entity - hold onto this name:
                    ent_name = e.get('name')

                if 'Component' in e.tag:
                    # form complete comp name:
                    comp_name = '{}.{}'.format(ent_name, e.get('name'))
                    id = e.get('id')
                    step_dict[comp_name] = int(id)

                    #print(comp_name)

    return step_dict


def xml_iterate_get_all_step_data(file_name):
    """
    Create a list for every step found in res file
    Run with/without the elem.clear() below
    :param file_name:
    :return:
    """

    step_tag = ns + 'Step'

    for event, elem in etree.iterparse(file_name):

        step_data = []

        if elem.tag == step_tag:
            # Just processed step, print it:
            print('------ Step: --------')
            #print elem.text
            #print '------ end Step ------'

            lines = elem.text.splitlines()

            for line in lines:
                step_data.extend(line.split())

            # done with that elem - try to free up memory:
            elem.clear()
            #print 'List all data, one step: Found {} elements'.format(len(step_data))
            #print step_data

            # Uncomment to only do this once!:
            # break

    return


def write_components_to_file(res_file, flg_header, flg_mag, comp_list, ucf_list, to_file):   ###
    """
    Find all components in comp_list, write to file
    :param res_file: path to .res file, str
    :param flg_header: flag, int, 1
    :param flg_mag: flag, int, 1
    :param comp_list: list of strings of componets (each component in string divided by space)
    :param ucf_list: list of strings of ucf (each component in string divided by space)
    :param to_file: list of strings of output file path (each component in string divided by space)
    :return:
    """

    tstart = time.time()
    print('---------- Getting stepmap dictionary: ---------')
    comp_dict = get_stepmap_dictionary(res_file)
    print('---------- Found dictionary in {:.2f} -----'.format(time.time() - tstart))

    print('Check if requested components are found in the res file dictionary: ')
    tstart = time.time()
    for cc in comp_list:
        comp_temp = cc.strip().split()
        for c in comp_temp:
            print("element {} is {} in the dictionary".format(c, c in comp_dict.keys()))
    print('---------- Dictionary existence check took: {:.2}'.format(time.time()-tstart))

    #    data_sep = ', '    # use for CSV file
    data_sep = '    '
    print('flg_mag : ', flg_mag)
    print('flg_header : ', flg_header)

    step_tag = ns + 'Step'
    print('step_tag = : {} '.format (step_tag) )
    print('---------- Start stepping through res file: ---------')
    tstart = time.time()
    data_vector_all = []
    all_comp_output_nr_list = []
    for event, elem in etree.iterparse(res_file):
        step_data = []
        if elem.tag == step_tag:
            lines = elem.text.splitlines()
            for line in lines:
                step_data.extend(line.split())
                elem.clear()  #done with that elem - try to free up memory:
            outp_nr = -1
            for outp_c in comp_list:
                data_vector = []
                ii = 0
                outp_nr = outp_nr + 1
                comp_temp2 = outp_c.strip().split()
                for comp_name in comp_temp2: #Get data comps from step_data:
                    # try:
                    id = comp_dict[comp_name]
                    id = id - 1  # Python is zero-based, but View starts from 1
                    ucf_list_ = str(ucf_list[outp_nr]).strip().split()
                    val_data = float(step_data[id]) * float(ucf_list_[ii])
                    # data_vector.append(step_data[id])
                    data_vector.append(str(val_data))
                    ii = ii + 1
                    # except:
                    #    data_vector.append(' ')
                if flg_mag == 1:  # MS------- acc magnitude calculate & write to file
                    # mag = math.sqrt(float(data_vector[1])*float(data_vector[1]) + float(data_vector[2])*float(data_vector[2]) + float(data_vector[3])*float(data_vector[3]))
                    mag = math.sqrt(float(data_vector[-1]) * float(data_vector[-1]) + float(data_vector[-2]) * float(data_vector[-2]) + float(data_vector[-3]) * float(data_vector[-3]))
                    data_vector.append(str(mag))
                if outp_nr not in all_comp_output_nr_list:
                    all_comp_output_nr_list.append(outp_nr)
                    data_vector_all.append(data_vector)
                else:
                    data_vector_all[outp_nr].extend("#")
                    data_vector_all[outp_nr].extend(data_vector)

    for i_nr, outp_f in enumerate(data_vector_all):
        print("writing file number: {0}".format(i_nr+1))
        file_out_name = str(to_file[i_nr]).strip().replace("\n", "")
        with open(file_out_name, mode='w') as outp_file:
            if flg_mag == 1:
                header_list = comp_list[i_nr].strip().split() + ['Vec_Mag']
            else:
                header_list = comp_list[i_nr].strip().split()
            if flg_header == 1:
                print('header_list : ', header_list)
            outp_file.write('# {}\n'.format(data_sep.join(header_list)))
            data_vector_temp_list1 = '*'.join(map(str, outp_f))
            data_vector_temp_list = data_vector_temp_list1.strip().split("#")
            for data_vect in data_vector_temp_list:
                temp = data_vect.strip("*").split("*")
                outp_file.write('{}\n'.format(data_sep.join(temp)))
    print('---------- Stepping through file took: {:.2f}s'.format(time.time()-tstart))





def get_component(res_file, comp_name):
    """
    """

    comp_dict = get_stepmap_dictionary(res_file)
    print(comp_dict)

    try:
        comp_id = comp_dict[comp_name]
    except KeyError:
        return []

    comp_id = comp_id - 1

    res = []

    step_tag = ns + 'Step'

    for event, elem in etree.iterparse(res_file):

        step_data = []

        if elem.tag == step_tag:

            lines = elem.text.splitlines()

            for line in lines:
                step_data.extend([float(i) for i in line.split()])
                # done with that elem - try to free up memory:
                elem.clear()

            res.append(step_data[comp_id])

    return res


def get_contact_incidents(res_file):

    # open text file for output??

    for event, elem in etree.iterparse(res_file):

        inc_tag = ns + 'Contact'
        #inc_data = []

        if elem.tag == inc_tag:

            inc_data = elem.text.split()

            print('Slip velocity is: {}'.format(inc_data[-2]))

            return


    return






if __name__ == '__main__':

    input_file = ''
    flg_header = 0
    flg_mag = 0
    #component_name = ''


    if len(sys.argv) == 2:
        arg_file_input = sys.argv[1]
        if not os.path.isfile(arg_file_input):
            print("given file doesn't exist: {0}".format(arg_file_input))
        else:
            with open(arg_file_input, "r") as input_data:
                all_input_data = input_data.readlines()
            input_file = all_input_data[0].strip()
            flg_header = int(all_input_data[1].strip())
            flg_mag = int(all_input_data[2].strip())
            output_files_nr = int(len(all_input_data[3:])/3)  #for each output starting in line 4 of input.txt: output_file_dir_name, comp_list, comp_list_UCF
            all_components_list, all_comp_ucf_list, all_outp_dir_names_list = [], [], []
            for ii in range(0, output_files_nr):
                all_outp_dir_names_list.append(all_input_data[3*ii+1+2])
                all_components_list.append(all_input_data[3*ii+2+2])
                all_comp_ucf_list.append(all_input_data[3*ii+3+2])
            write_components_to_file(input_file, flg_header, flg_mag, all_components_list, all_comp_ucf_list, all_outp_dir_names_list)
    else:
        print("2 arguments need to be given: python script name and input file name!")

    if input_file:
        if verbose:
            d = get_stepmap_dictionary(input_file)
            print('-' * 10 + ' Results file contains components named:')
            print(d)

        # if component_name:
        #     r = get_component(input_file, component_name)
        #     print('-' * 10 + ' Result {} has these values:'.format(component_name))
        #     print(r)

    # xml_iterate_print_all_tags(filename)

    # uncommment to print the stepmap dictionary:
    #xml_iterate_print_stepmap(filename)

    # uncomment to load up each piece of data & then discard.
    # Use with/out the elem.clear() call to see memory usage
    # xml_iterate_get_all_step_data(filename)
    # time.sleep(10)

    # uncomment to get the complete stepmap dictionary:
    # d = get_stepmap_dictionary(filename)
    # print d

    # try to get all contact incidents:
    # get_contact_incidents('test_001.res')


