from argparse import ArgumentParser
from mape_maker.MapeMaker import MapeMaker
from mape_maker.utilities.Scenarios import Scenarios
import logging
import sys
import os


def make_parser():
    parser = ArgumentParser()
    # path
    parser.add_argument('-xf', '--input_xyid_file',
                        help='input file for simulation',
                        type=str,
                        required=True)
    parser.add_argument('-sf', '--input_sid_file',
                        help='second input file for simulation,\
                         from which scenarios for the other timeseries are generated',
                        type=str,
                        default=None)
    parser.add_argument('-o', '--output_dir',
                        help='path to a directory to save the simulations',
                        type=str,
                        default=None)
    parser.add_argument('-vo', '--verbosity_output',
                        help='the output file to save the verbosity',
                        type=str,
                        default=None)
    # datetime
    parser.add_argument('-is', '--input_start_time',
                        help='start time for computation of the distribution',
                        type=str,
                        default=None)
    parser.add_argument('-ie', '--input_end_time',
                        help='end time for computation of the distribution',
                        type=str,
                        default=None)
    parser.add_argument('-ss', '--simulation_start_time',
                        help='start time for simulation',
                        type=str,
                        default=None)
    parser.add_argument('-se', '--simulation_end_time',
                        help='end time for simulation',
                        type=str,
                        default=None)
    # numeric input
    parser.add_argument('-t', '--target_mape',
                        help='mape you want in return, otherwise will take the mape of the dataset',
                        type=float,
                        default=None)
    parser.add_argument('-a', '--a',
                        help='percent of data for the estimation',
                        type=float,
                        default=4)
    parser.add_argument('-ct', '--curvature_target',
                        help='target of the second difference',
                        type=float,
                        default=None)
    parser.add_argument('-m', '--mip_gap',
                        help='the curvature mip gap',
                        type=float,
                        default=0.3)
    parser.add_argument('-n', '--simulations_num',
                        help='number of simulations',
                        type=int,
                        default=1)
    parser.add_argument('-tl', '--time_limit',
                        help='time limit for computing curvature',
                        type=int,
                        default=3600)
    parser.add_argument('-ps', '--plot_start_date',
                        help='start date to plot the result',
                        type=int,
                        default=0)
    parser.add_argument('-s', '--seed',
                        help='seed for simulation',
                        type=int,
                        default=None)
    parser.add_argument('-v', '--verbosity',
                        help='verbosity level',
                        type=int,
                        default=2)
    # boolean
    parser.add_argument('-f', '--sid_feature',
                        help='feature for simulation',
                        choices=['actuals', 'forecasts'],
                        default='actuals')
    parser.add_argument('-bp', '--base_process',
                        help='method used',
                        choices=['iid', 'ARMA'],
                        default='ARMA')
    parser.add_argument('-lp', '--load_pickle',
                        help='load pickle file instead of estimating',
                        default=False,
                        action='store_true')
    parser.add_argument('-c', '--curvature',
                        help='curvature',
                        default=False,
                        action='store_true')
    parser.add_argument('-sh', '--show_curv_model',
                        help='show model of curvature',
                        default=False,
                        action='store_true')
    parser.add_argument('-p', '--plot',
                        help='plot simulations',
                        default=True,
                        action='store_false')
    # other param
    parser.add_argument('-sv', '--solver',
                        help='curvature solver',
                        default='gurobi')
    parser.add_argument('-tt', '--title',
                        help='title for the plot',
                        default=None)
    parser.add_argument('-xl', '--x_legend',
                        help='x legend for the plot',
                        default=None)
    parser.add_argument('-sb', '--scale_by_capacity',
                        help='scale by capacity instead of observation '
                        'optionally enter the capacity (enter 0 to use max)',
                        type=float,
                        default=None)
    return parser


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


def main(args):
    #print(f'capacity entriy was {args.scale_by_capacity}')
    # quit()
    logger = logging.getLogger('mape-maker')
    logger = set_verbose_level(logger, args.verbosity, args.verbosity_output)
    mare_embedder = MapeMaker(logger=logger,
                              xyid_path=args.input_xyid_file,
                              ending_feature=args.sid_feature,
                              xyid_load_pickle=args.load_pickle,
                              input_start_dt=args.input_start_time,
                              input_end_dt=args.input_end_time,
                              a=args.a,
                              base_process=args.base_process,
                              scale_by_capacity=args.scale_by_capacity)
    if args.curvature:
        pyomo_param = {
            "MIP": args.mip_gap,
            "time_limit": args.time_limit,
            "curvature_target": args.curvature_target,
            "solver": args.solver,
        }
    else:
        logger.warning(
            "You have not set curvature to be true, so curvature is not used.")
        pyomo_param = None
    tmare = args.target_mape / 100 if args.target_mape is not None else None
    results = mare_embedder.simulate(sid_file_path=args.input_sid_file,
                                     simulation_start_dt=args.simulation_start_time,
                                     simulation_end_dt=args.simulation_end_time,
                                     output_dir=args.output_dir,
                                     seed=args.seed,
                                     n=args.simulations_num,
                                     curvature_parameters=pyomo_param,
                                     show=args.show_curv_model,
                                     r_tilde=tmare)

    x_legend = mare_embedder.xyid.x_name if args.x_legend is None else args.x_legend
    Scenarios(X=mare_embedder.sid.x_t,
              Y=mare_embedder.sid.y_t,
              results=results,
              target_mare=mare_embedder.sid.SimParams.r_tilde,
              f_mare=mare_embedder.xyid.dataset_info.get(
                  "r_m_hat"),
              plot_start_date=args.plot_start_date,
              output_dir=args.output_dir,
              plot=args.plot,
              title=args.title,
              x_legend=x_legend,
              ending_feature=args.sid_feature,
              logger=logger,
              scale_by_capacity=args.scale_by_capacity,
              cap=mare_embedder.xyid.dataset_info.get("cap"))


if __name__ == '__main__':
    parser = make_parser()
    args = parser.parse_args()
    main(args)
