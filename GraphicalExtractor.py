import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
from datetime import date
class GraphicalExtractor(object):

    def __init__(self):
        self.columns_effiency = ["cpu_usage", "ram_usage", "amount_of_data", "time"]
        self.columns_analyze = []

    def __create_pdf(self, evaluator_outcome, analyzer_outcome, output_file_type, output_filename, output_path):
        effiency_df = pd.DataFrame.from_dict(evaluator_outcome["efficiency"], orient='index', columns=self.columns_effiency)
        fig, ax = plt.subplots(4, 2, figsize=(15,40))
        for i in range(4):
            ax[i, 0].plot(effiency_df.index, effiency_df.iloc[:, i], c="c", marker="D")
            ax[i, 0].set_title(self.columns_effiency[i])
            ax[i, 0].set_xlabel("Amount of data")
            ax[i, 0].set_ylabel(self.columns_effiency[i])
            ax[i, 1].bar(effiency_df.index, effiency_df.iloc[:, i], color="c")
            ax[i, 1].set_title(self.columns_effiency[i])
            ax[i, 1].set_xlabel("Amount of data")
            ax[i, 1].set_ylabel(self.columns_effiency[i])
        plt.savefig(output_path + output_filename+ "." + output_file_type, format=output_file_type)
    
    def extract(self, output_file_type, output_filename, output_path, evaluator_outcome, analyzer_outcome):
        self.__create_pdf(evaluator_outcome, analyzer_outcome, output_file_type, output_filename, output_path)