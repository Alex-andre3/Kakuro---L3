class Grid:
    def __init__(self, filename, width=0, length=0, grid=[]):
        self.filename = filename
        self.width = width
        self.length = length
        self.grid = grid

    def set_width(self, width):
        self.width = width

    def set_length(self, length):
        self.length = length

    def get_grid(self):
        return self.grid

    def grid_maker(self):

        try:
            file = open(self.filename, "r")

            lignes = file.readlines()
            witdh = len(lignes)

            for ligne in lignes:
                modif_ligne = ligne.split("_")

                # Now, we know the grid length
                self.set_length(len(modif_ligne))

                for lignas in modif_ligne:
                    if "/" not in lignas:
                        tmp = int(lignas)
                        if tmp == -1:
                            self.grid.append("ici il faut ajouter l'objet case")

        except ValueError:
            print("Ooops ! Grossière erreur dans votre code.")





