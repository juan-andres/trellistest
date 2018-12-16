class Image:
    def __init__(self, width=16, height=16):
        self.width = width
        self.height = height
        self.pixel_data = []
        for string_row in [
            "   *    *     * ",
            " * * *  *     * ",
            "   *    *     * ",
            "   *    *     * ",
            "   *    *     * ",
            "   *    *     * ",
            "   *    *     * ",
            "   *    *     * ",
            "   *    *     * ",
            "   *    *     * ",
            "   *    *     * ",
            "   *    *     * ",
            "   *    *     * ",
            "   *    *     * ",
            "   *    *     * ",
            "   *    *     * ", ]:
            row = []
            for c in string_row:
                if c == " ":
                    color = 0x000
                else:
                    color = 0xF00
                row.append(color)
            self.pixel_data.append(row)
