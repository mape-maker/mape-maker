from pylatex import Document, PageStyle, Head, MiniPage, Section, Subsection, Table, Math, TikZ, Axis, \
    Plot, Figure, Matrix, Alignat, Package, Command, Tabular, Center
from pylatex.utils import italic, escape_latex, NoEscape, bold
from pylatex.frames import MdFramed


def generate_unique(name, df, version):
    geometry_options = {
        "head": "5pt",
        "margin": "1in",
        "bottom": "1in",
        "includeheadfoot": True
    }
    doc = Document(geometry_options=geometry_options)
    # Generating first page style

    doc.preamble.append(Command('title', 'MapeMaker {}'.format(version)))
    doc.preamble.append(Command('author', 'Name of the simulator : {}'.format(name)))
    doc.preamble.append(Command('date', NoEscape(r'\today')))
    doc.append(NoEscape(r'\maketitle'))

    summary_text = "Dataset used : {}\n" \
                   "Predicting {} from {}\n" \
                   "Date_Ranges simulated from {} to {}\n" \
                   "With Base Process {}\n" \
                   "Computed {} simulations".format(
                                                      df['parameters']["input_file"],
                                                      df['parameters']["x"],
                                                      df['parameters']["y"],
                                                      df['parameters']["date_range"][0][0].strftime("%Y-%m-%d"),
                                                      df['parameters']["date_range"][0][1].strftime("%Y-%m-%d"),
                                                      df['parameters']["base_process"],
                                                      len(df['mare']["scores_mare"]),
                                                    )

    if df['parameters']['output_file'] is not None:
        summary_text += "\nOutput stored in {}\n".format(df['parameters']['output_file'])

    if df["parameters"]["curvature_parameters"] is not None:
        curvature_parameters = df["parameters"]["curvature_parameters"]
        summary_text += "\n\n Smoothness correction  used with parameters :\n" \
                        "    * Solver used : {}\n" \
                        "    * MIP Gap used : {}\n"\
                        "    * TimeLimit used : {}\n".format(
                            curvature_parameters["solver"],
                            curvature_parameters["MIP"],
                            curvature_parameters["time_limit"]
                            )

    with doc.create(Section('Parameters of the simulations')):
        doc.append(MdFramed(arguments=summary_text))

    with doc.create(Section('Raw Results')):
        doc.append('The simulations were computed between {} and {}, for {} samples\n'.format(df['parameters']["date_range"][0][0].strftime("%Y-%m-%d"),
                                                                                            df['parameters']["date_range"][0][1].strftime("%Y-%m-%d"),
                                                                                            df['n']))

        with doc.create(Subsection('Target Mape')):
            mares = df['mare']
            doc.append('The target mape was {}%, the observed mape for '
                       'the range of dates asked for is {}%\n'.format(100*mares["target_mare"],
                                                                   100*mares["observed_mare"]))
            with doc.create(Center()) as centered:
                with centered.create(Tabular('|c|c|c|')) as table:
                    table.add_hline()
                    table.add_row(("simulations", "simulated mape", "score"), mapper=bold, color="lightgray")
                    table.add_hline()
                    for i in range(len(mares["simulated_mares"])):
                        table.add_row("simulation n {}".format(i+1), "{}%".format(round(100*mares["simulated_mares"][i], 1)),
                                        mares["scores_mare"][i])
                    table.add_empty_row()
                    table.add_hline()

        with doc.create(Subsection('Target Smoothness')):
            curvature = df['curvature']
            if curvature["target_second_differences"] is None :
                doc.append("There was no target for curvature")
            else:
                doc.append('The target second difference was {}, the observed second difference for '
                           'the range of dates asked for is {}\n'.format(round(curvature["target_second_differences"],1),
                                                                       curvature["observed_second_differences"]))
                with doc.create(Center()) as centered:
                    with centered.create(Tabular('|c|c|c|')) as table:
                        table.add_hline()
                        table.add_row(("simulations", "simulated second difference", "score"), mapper=bold, color="lightgray")
                        table.add_hline()
                        for i in range(len(curvature["simulated_second_differences"])):
                            table.add_row("simulation n {}".format(i+1), "{}".format(curvature["simulated_second_differences"][i]),
                                            curvature["scores_curvature"][i])
                        table.add_empty_row()
                        table.add_hline()

        with doc.create(Subsection('Auto Correlation')):
            auto_corr = df['error_auto_correlation']
            doc.append('The target for the autocorrelation of relative errors was {}\n'.format(
                auto_corr["target_auto_correlation"][0]))

            with doc.create(Center()) as centered:
                with centered.create(Tabular('|c|c|c|')) as table:
                    table.add_hline()
                    table.add_row(("simulations", "simulated auto-correlation", "score"), mapper=bold, color="lightgray")
                    table.add_hline()
                    for i in range(len(auto_corr['scores_auto_correlation'])):
                        table.add_row("simulation n {}".format(i+1), auto_corr['simulated_auto_correlation'][i],
                                       auto_corr['scores_auto_correlation'][i])
                    table.add_empty_row()
                    table.add_hline()


    # with doc.create(Section('Table')):
    #     with doc.create(Table(position='htbp')) as table:
    #         table.add_caption('Test')
    #         table.append(Command('centering'))
    #         table.append(NoEscape(df.to_latex(escape=False)))


    return doc

