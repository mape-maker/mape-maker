import os
import sys
import click
#import MapeMaker as MapeMaker
from mape_maker import MapeMaker 
from datetime import datetime as dt
import logging, verboselogs


def click_callback(f):
    return lambda _, __, x: f(x)


def check_date(s):
    try:
        return dt.strptime(s, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise Exception(msg)
    except TypeError:
        return None


@click.command()
@click.argument('input_file')
@click.option('--second_file', "-sf", default=None, help = 'second input file with one timeseries only (e.g. actuals), from which scenarios for the other timeseries are generated (e.g. forecasts)')
@click.option('--target_mape', "-t",  default=None, type=float, help='mape you want in return otherwise will take the mape of the dataset')
@click.option('--simulated_timeseries','-st', default="actuals", help="feature you want to simulate 'actuals' or 'forecasts'")
@click.option('--base_process', '-bp', default="ARMA", help="method used to this end 'iid' or 'ARMA")
@click.option('--a', '-a', default=4, type=float, help="percent of data on the left or on the right for the estimation")
@click.option('--output_dir', "-o", default=None, help="path to a directory to save the simulations")
@click.option('--number_simulations', '-n', default=1, help="number of simulations")
@click.option('--input_start_dt', '-is', default=None, callback=click_callback(check_date), help="start_date for the computation of the distributions, format='Y-m-d %H:%M:%S' ")
@click.option('--input_end_dt', '-ie', default=None, callback=click_callback(check_date), help="end_date for the computation of the distributions, format='Y-m-d %H:%M:%S'")
@click.option('--simulation_start_dt', '-sd', default=None, callback=click_callback(check_date), help="start_date for the simulation, format='Y-m-d %H:%M:%S' ")
@click.option('--simulation_end_dt', '-ed', default=None, callback=click_callback(check_date), help="end_date for the simulation, format='Y-m-d %H:%M:%S'")
@click.option('--title', '-ti', default=None, help="title for the plot")
@click.option('--seed', '-s', default=None, help="random seed")
@click.option('--load_pickle', '-lp', default=False, type=bool, help="Load the pickle file instead of estimating")
@click.option('--curvature', '-c', default=False, help="curvature")
@click.option('--time_limit', '-tl', default=3600, help="time limit of the computation of curvature")
@click.option('--curvature_target', '-ct', default=None, type=float, help="the target of the second difference")
@click.option('--mip_gap', '-m', default=0.3, type=float, help="the curvature mip gap")
@click.option('--solver', '-so', default="gurobi", help="curvature solver")
###@click.option('--full_dataset', '-fd', default=False, type=bool, help="simulation over all the dataset")
@click.option('--latex_output', '-lo', default=False, type=bool, help="write results in latex file")
@click.option('--show', '-sh', default=True, type=bool, help="plot simulations")
@click.option('--verbosity', '-v', default=2, type=int, help="verbosity level")
@click.option('--verbosity_output', '-vo', default=None, help="the output file to save the verbosity")


def main(input_file, second_file, target_mape, simulated_timeseries, base_process, a, output_dir, number_simulations, input_start_dt,
         input_end_dt, simulation_start_dt, simulation_end_dt, title, seed, load_pickle, curvature, time_limit, curvature_target,
         mip_gap, solver, latex_output, show, verbosity, verbosity_output):
    return main_func(input_file, second_file, target_mape, simulated_timeseries, base_process, a, output_dir, number_simulations,
                     input_start_dt, input_end_dt, simulation_start_dt, simulation_end_dt, title, seed, load_pickle,
                     curvature, time_limit, curvature_target, mip_gap, solver, latex_output, show, verbosity, verbosity_output)

def set_verbose_level(logger, verbosity, verbosity_output):
    format = '%(message)s'
    if verbosity == 2:
        level = logging.INFO
    elif verbosity == 1:
        level = logging.WARNING
    elif verbosity == 0:
        level = logging.ERROR
    else:
        print("{}, Undefined verbosity level".format(verbosity))
        sys.exit(1)
    if verbosity_output is not None:
        # check whether the output file already exist
        if os.path.isfile(verbosity_output):
            # delete the existing file
            os.remove(verbosity_output)
        logging.basicConfig(filename=verbosity_output, level=level,
                            format=format)
    else:
        logging.basicConfig(level=level, format=format)
    return logger

def input_check(input_start_dt, input_end_dt, simulation_start_dt, simulation_end_dt, output_dir, second_file):
    """ Check some of the user inputs.
        TBD: get better date handling; delete this comment after Dec 2019
    """
    if (input_start_dt is None and input_end_dt is not None) \
       or (input_start_dt is not None and input_end_dt is None):
        raise RuntimeError\
            ("You must give both or neither of the input dates")
    if (simulation_start_dt is None and simulation_end_dt is not None) \
       or (simulation_start_dt is not None and simulation_end_dt is None):
        raise RuntimeError\
            ("You must give both or neither of the simulation dates")
    if simulation_start_dt is not None\
       and input_start_dt is not None\
       and simulation_start_dt < input_start_dt\
       and second_file is None:
        raise RuntimeError ("Simulation must start after input start")
    if output_dir is not None and os.path.exists(output_dir):
        raise RuntimeError ("Output directory={} already exists".format(output_dir))
    if second_file is not None:
        if simulation_start_dt is None or simulation_end_dt is None:
            raise RuntimeError("You must give both the simulation dates for the second file")

def main_func(input_file, second_file, target_mape, simulated_timeseries, base_process, a, output_dir, number_simulations, input_start_dt,
              input_end_dt, simulation_start_dt, simulation_end_dt, title, seed, load_pickle, curvature, time_limit, curvature_target,
         mip, solver, latex_output, show, verbosity, verbosity_output):
    logger = logging.getLogger('mape-maker')
    logger = set_verbose_level(logger, verbosity, verbosity_output)
    input_check(input_start_dt, input_end_dt, simulation_start_dt, simulation_end_dt, output_dir, second_file)
    if simulation_start_dt is None and input_start_dt is not None:
        simulation_start_dt = input_start_dt
    if simulation_end_dt is None and input_end_dt is not None:
        simulation_end_dt = input_end_dt
    full_dataset = simulation_start_dt is None and simulation_end_dt is None
        
    mare_embedder = MapeMaker.MapeMaker(logger,
                                        path=input_file,
                                        ending_feature=simulated_timeseries,
                                        load_pickle=load_pickle,
                                        seed=seed,
                                        input_start_dt=input_start_dt,
                                        input_end_dt=input_end_dt
                                        )
    if curvature:
        pyomo_parameters = {
                "MIP": mip,
                "time_limit": time_limit,
                "curvature_target": curvature_target,
                "solver": solver,
            }
    else:
        pyomo_parameters = None

    tmare = target_mape/100 if target_mape is not None else None

    list_of_date_ranges = [[simulation_start_dt, simulation_end_dt]]
    scores = mare_embedder.simulate(second_file=second_file, target_mare=tmare, base_process=base_process, n=number_simulations,
                                    full_dataset=full_dataset, output_dir=output_dir,
                                    list_of_date_ranges=list_of_date_ranges, curvature_parameters=pyomo_parameters,
                                    latex=latex_output)

    t = mare_embedder.r_tilde
    text = "Dataset used : {}\n" \
           "Computed Mape from the dataset {}%\n" \
           "Mape fit from the dataset {}%\n" \
           "Target Mape : {}%\n" \
           "Simulated from {} to {}\n" \
           "With base process {}\n" \
           "Computed {} simulations from {} to {}".format(input_file,
                                                          round(100*mare_embedder.mare,2),
                                                          round(100*mare_embedder.r_m_hat,2), round(100*t,2),
                                                          mare_embedder.x, mare_embedder.y, base_process,
                                                          number_simulations, mare_embedder.start_date.strftime("%Y-%m-%d"),
                                                          mare_embedder.end_date.strftime("%Y-%m-%d"))

    logger.info(text)

    mare_embedder.save_all_outputs(output_dir)
    if output_dir is not None:
        text = text + "\nOutput stored in directory {}".format(output_dir)

    if show:
        mare_embedder.plot_example(title=title)

    return mare_embedder

if __name__ == "__main__":
    main()


