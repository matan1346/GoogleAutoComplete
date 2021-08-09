import pyodbc
#
missing_score = {0: 10, 1: 8, 2: 6, 3: 4}

def get_connection():

    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=server_name;'
                          'Database=database_name;'
                          'Trusted_Connection=yes;')

    return conn.cursor()



def search(q):

    #conn = get_connection()
    # cursor = conn.cursor()
    s = ''
    real_sentence = 'i @ like, to pLAy, games!'
    formatted_sentence = 'i like to play games'
    start_score = (len(formatted_sentence) - 1) * 2
    for pos in range(len(formatted_sentence)):
        current_score = start_score - 2
        if pos <= 3:
            current_score = start_score - missing_score[pos]

        piece_missing_char = formatted_sentence[:pos] + formatted_sentence[pos + 1:]

        s += f" OR LIKE '%{piece_missing_char}%'"

        # insert_to_db(piece_misssing_char, sentence, file_path, current_score)

        # insert dot for addition char
        piece_addition_char = formatted_sentence[:pos] + '_' + formatted_sentence[pos + 1:]
        s += f" OR LIKE '%{piece_addition_char}%'"
        # print('\t\t', piece_misssing_char)
        # print('\t\t', piece_addition_char)
        #insert_to_db(piece_addition_char, sentence, file_path, current_score)
    print(f"SELECT * FROM T_Data WHERE KeySentence LIKE '%{formatted_sentence}%'" + s)
    #cursor.execute(f"SELECT * FROM T_Data WHERE KeySentence LIKE '%{formatted_sentence}%'")

    #for row in cursor:
    #    print(row)



def main():
    search('lol')



if __name__ == '__main__':
    main()