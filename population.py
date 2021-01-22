import numpy as np
import matplotlib.pyplot as plt


def printResult(f):
    def wrapper(*args, **kwargs):
        result = f(*args, **kwargs)
        plt.show()
        print(', '.join(result[1]))
        return result

    return wrapper


class Population:
    def __init__(self, years_path, countries_path, population_path):
        # read file
        self.years = np.genfromtxt(years_path, delimiter=',', dtype='uint64')
        self.countries = np.genfromtxt(countries_path, delimiter=',', dtype='U')
        self.population = np.genfromtxt(population_path, delimiter=',', dtype='uint64')

        # sort by year
        order = np.argsort(self.years)
        self.years = self.years[order]
        self.population = self.population[:, order]
        del order

        # median population
        self.median_pop = np.median(self.population, axis=0)

        # regions
        self.regions = np.unique(self.countries[:, 2])
        self.regions_populations = None
        for region in self.regions:
            temp = np.sum(self.population[np.where(self.countries[:, 2] == region)], axis=0)
            temp = temp.reshape([1, temp.shape[0]])
            if self.regions_populations is None:
                self.regions_populations = temp
            else:
                self.regions_populations = np.append(self.regions_populations, temp, axis=0)
            del temp

        # top 10 population in 2019
        self.curt10_idx = np.argsort(self.population[:, np.where(self.years == 2019)[0][0]])[-10:]

        # top 2 population growth
        self.growt2 = self.topn_population_growth(2)

    def countries_trends(self, idxs):
        assert len(idxs) != 0, 'At last select a country'
        return self.countries[idxs], self.population[idxs]

    def topn_population_growth(self, n):
        difference = np.subtract(self.population[:, -1], self.population[:, 0], dtype='int64')
        topn = np.flipud(np.argsort(difference))[:n]
        return topn, difference[topn]

    def cidx_lookup_name(self, name):
        return np.where(self.countries[:, 0] == name)[0][0]

    def cidx_lookup_code(self, code):
        return np.where(self.countries[:, 1] == code)[0][0]

    def figure_select_trends(self, country_idx):
        countries, population = self.countries_trends(country_idx)
        countries = np.append(countries[:, 0], ['Median'])
        population = np.append(population, self.median_pop.reshape([1, self.median_pop.shape[0]]), axis=0)
        fig = self.plot(population, countries, self.years, 'Population (millions)', 'Year', 'Population for Selected Countries')
        return fig

    @printResult
    def figure_regions_trends(self):
        fig = self.plot(self.regions_populations, self.regions, self.years, 'Population (millions)', 'Year', 'Population for All Regions')
        return fig, self.regions

    @printResult
    def figure_top10_trends(self):
        countries, population = self.countries_trends(self.curt10_idx)
        countries = countries[:, 0]
        fig = self.plot(population, countries, self.years, 'Population (millions)', 'Year', 'Population for Top 10 Countries')
        return fig, countries

    @printResult
    def figure_gtop2_trends(self):
        countries, population = self.countries_trends(self.growt2[0])
        countries = countries[:, 0]
        fig = self.plot(population, countries, self.years, 'Population (millions)', 'Year', 'Population for Growth Top 2 Countries')
        return fig, countries

    @staticmethod
    def plot(values, labels, x_value, y_label, x_label, title):
        million_v = values / 10 ** 6
        fig = plt.figure(figsize=(10, 7), dpi=200)
        ax = fig.add_subplot(1, 1, 1)
        for i in range(million_v.shape[0]):
            ax.plot(x_value.astype('S'), million_v[i], label=labels[i])
        # ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(title)
        plt.xticks(rotation=90)
        plt.legend(loc='upper left')
        return fig


if __name__ == '__main__':
    p = Population('references//years.csv', 'references//countries.csv', 'references//population.csv')
    p.figure_select_trends([92, 93])
    p.figure_regions_trends()
    p.figure_top10_trends()
    p.figure_gtop2_trends()
