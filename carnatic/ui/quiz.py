import csv
import random
from carnatic import settings
from PyQt6 import QtTest
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6 import QtGui
from PyQt6.QtGui import QFont, QAction, QIcon
quiz_file = settings._CONFIG_PATH + 'quiz_bank.db'
_MAX_ANSWERS = 6
_GREEN_CHECK = u'\u2705  '
_RED_CROSS = u'\u274C  '
_ANSWER_CHECK = lambda rc : '\t' + _GREEN_CHECK if rc else '\t' + _RED_CROSS
class QuizUI(QDialog):
    def __init__(self,question_count=10):
        super().__init__()
        self._resources = settings._RESOURCES
        self.setWindowTitle(self._resources['lblQuiz'])
        self.setMinimumSize(400, 400)
        self._quiz_db = _get_quiz_db()
        self._question_count = question_count
        self._questions = _get_random_questions(self._quiz_db, self._question_count)
        self._initialize_all_widgets()
        self._show_ui()
    def _initialize_all_widgets(self):
        self._question_header = QLabel(self._resources['lblQuestion'])
        self._question_label = QLabel('')
        self._question_groupbox = QGroupBox()
        self._multichoice_groupbox = QGroupBox()        
        self._cryptic_groupbox = QGroupBox()
        self._answer_label = QLabel(self._resources['lblAnswer'])
        self._answer_text = QLineEdit('')
        self._correct_answer_groupbox = QGroupBox()
        self._correct_answer_label1 = QLabel(self._resources['lblCorrectAnswer'])
        self._correct_answer_label2 = QLabel('')
        self._correct_answer_label3 = QLabel('')
        self._credits_groupbox = QGroupBox()
        self._credits_label = QLabel(self._resources['lblCredits']+':')
        self.answer_button = QPushButton(self._resources['lblAnswer'])
        self.answer_button.clicked.connect(self._answer_clicked)
        self._previous_button = QPushButton(self._resources['lblPrevious'])
        self._previous_button.clicked.connect(self._previous_clicked)
        self._next_button = QPushButton(self._resources['lblNext'])
        self._next_button.clicked.connect(self._next_clicked)
        self._close_button = QPushButton(self._resources['lblClose'])
        self._close_button.clicked.connect(self._close_clicked)
        self._button_group = QGroupBox()
        self._summary_label = QLabel(self._resources['lblSummaryOfQuiz'])
        self._summary_table = QTableWidget(3,2)
        self._summary_table.setColumnWidth(0,200)
        self._summary_group = QGroupBox()
    def _show_ui(self):
        self._question_index = 0
        self._v_layout = QVBoxLayout()
        self._show_question_ui()
        self._show_cryptic_answer_ui()
        self._show_multiple_choice_answer_ui()
        h_layout = QHBoxLayout()
        h_layout.addWidget(self._correct_answer_label1)
        h_layout.addWidget(self._correct_answer_label2)
        h_layout.addWidget(self._correct_answer_label3)
        self._correct_answer_groupbox.setLayout(h_layout)
        self._v_layout.addWidget(self._correct_answer_groupbox)
        h_layout = QHBoxLayout()
        h_layout.addWidget(self._credits_label)
        self._credits_groupbox.setLayout(h_layout)
        self._v_layout.addWidget(self._credits_groupbox)
        self._question_index = 0 
        self._user_answers = [('','') for _ in range(self._question_count)]
        self._correct_answers = ['' for _ in range(self._question_count)]
        self._summary_ui()
        self._button_ui()
        self.setLayout(self._v_layout)
        self._update_question()
    def _button_ui(self):
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.answer_button)
        h_layout.addWidget(self._previous_button)
        h_layout.addWidget(self._next_button)
        h_layout.addWidget(self._close_button)
        self._button_group.setLayout(h_layout)
        self._v_layout.addWidget(self._button_group)
    def _show_hide_summary_ui(self,show=True):        
        if show:
            self._question_groupbox.hide()
            self._correct_answer_groupbox.hide()
            self._multichoice_groupbox.hide()
            self._cryptic_groupbox.hide()
            self._credits_groupbox.hide()
            self._button_group.show()
            self.answer_button.hide()
            self._next_button.setEnabled(False)
            self._summary_group.show()
        else:
            self._question_groupbox.show()
            self._correct_answer_groupbox.show()
            self._multichoice_groupbox.show()
            self._cryptic_groupbox.show()
            self._credits_groupbox.show()
            self._button_group.show()
            self.answer_button.show()
            self._next_button.setEnabled(True)
            self._summary_group.hide()            
    def _update_summary_ui(self):
        self._summary_table.setItem(0,0,QTableWidgetItem(self._resources['lblQuestionsTotal']))
        self._summary_table.setItem(0,1,QTableWidgetItem(str(self._question_count)))
        self._summary_table.setItem(1,0,QTableWidgetItem(self._resources['lblQuestionsAnswered']))
        questions_answered = sum([ a!='' or b!='' for (a,b) in  self._user_answers])      
        self._summary_table.setItem(1,1,QTableWidgetItem(str(questions_answered)))
        self._summary_table.setItem(2,0,QTableWidgetItem(self._resources['lblQuestionsAnsweredCorrect']))
        questions_answered_correct = sum([ a!='' and _GREEN_CHECK in b for (a,b) in  self._user_answers])
        self._summary_table.setItem(2,1,QTableWidgetItem(str(questions_answered_correct)))
        self.setFixedSize(self._v_layout.sizeHint())
        self._summary_table.resizeColumnToContents(1)
        self._summary_table.resizeRowsToContents()        
    def _summary_ui(self):
        self._show_hide_summary_ui(show=False)
        v_layout = QVBoxLayout()
        v_layout.addWidget(self._summary_label)
        self._summary_table.setEnabled(False)
        self._summary_table.horizontalHeader().hide()
        self._summary_table.verticalHeader().hide()
        v_layout.addWidget(self._summary_table)
        self._summary_group.setLayout((v_layout))
        self._v_layout.addWidget(self._summary_group)
        self._button_group.show()
    def _show_question_ui(self):
        v_layout = QVBoxLayout()
        v_layout.addWidget(self._question_header,Qt.AlignmentFlag.AlignTop+Qt.AlignmentFlag.AlignLeft)
        v_layout.addWidget(self._question_label,Qt.AlignmentFlag.AlignTop+Qt.AlignmentFlag.AlignLeft)
        self._question_groupbox.setLayout(v_layout)
        self._v_layout.addWidget(self._question_groupbox,Qt.AlignmentFlag.AlignTop+Qt.AlignmentFlag.AlignLeft)
    def _show_multiple_choice_answer_ui(self):
        v_layout = QVBoxLayout()
        choice_count = _MAX_ANSWERS
        self._choice_options = []
        for c in range(choice_count):
            self._choice_options.append(QRadioButton(''))
            self._choice_options[c].toggled.connect(self._user_answered)
            v_layout.addWidget(self._choice_options[c])
        self._multichoice_groupbox.setLayout(v_layout)
        self._v_layout.addWidget(self._multichoice_groupbox)
        self._cryptic_groupbox.hide()
    def _show_cryptic_answer_ui(self):
        h_layout = QHBoxLayout()
        h_layout.addWidget(self._answer_label)
        self._answer_text.editingFinished.connect(self._user_answered)
        h_layout.addWidget(self._answer_text)
        self._cryptic_groupbox.setLayout(h_layout)
        self._v_layout.addWidget(self._cryptic_groupbox)
        self._multichoice_groupbox.hide()
        self._v_layout.addLayout(h_layout) 
    def _get_id_of_multiple_choice(self):
        for i,radio_button in enumerate(self._choice_options):
            if radio_button.isChecked():
                return i
        return '' 
    def _user_answered(self):
        question = self._questions[self._question_index]
        correct_answer = question['correct_answer']
        if int(question['type'])==2:
            user_answer = int(self._get_id_of_multiple_choice())
            self._user_answers[self._question_index] = (user_answer,'')
        else:
            user_answer = self._answer_text.text()
            self._user_answers[self._question_index] = (user_answer,'')
        #self._update_question()
        self.answer_button.setFocus()
    def _answer_clicked(self):
        question = self._questions[self._question_index]
        correct_answer = question['correct_answer']
        user_answer = self._user_answers[self._question_index][0]
        if int(question['type'])==2:
            correct_answer = int(correct_answer)
            correct_answer_text = self._choice_options[correct_answer].text()
            self._correct_answers[self._question_index] = correct_answer
            self._user_answers[self._question_index] = self._user_answers[self._question_index][0],_ANSWER_CHECK(user_answer==correct_answer)
        else:
            self._correct_answers[self._question_index] = correct_answer
            correct_answer_text = correct_answer
            self._user_answers[self._question_index] = (user_answer,_ANSWER_CHECK(user_answer.strip().lower()==correct_answer.strip().lower()))
        self._correct_answer_label2.setText(correct_answer_text)
        self._correct_answer_label3.setText(self._user_answers[self._question_index][1])
    def _block_radio_signals(self,block=True):
        for r in range(_MAX_ANSWERS):
            self._choice_options[r].blockSignals(block)
        
    def _update_question(self):
        self._previous_button.setEnabled(True)
        if self._question_index==0:
            self._previous_button.setEnabled(False)
        self._question_header.setText(self._resources['lblQuestion']+'-'+str(self._question_index+1))
        question = self._questions[self._question_index]
        self._question_label.setText(question['question'])
        #self.setFixedSize(self._v_layout.sizeHint())
        user_answer = self._user_answers[self._question_index]
        correct_answer = self._correct_answers[self._question_index]
        if int(question['type'])==2:
            self._cryptic_groupbox.hide()
            self._multichoice_groupbox.show()
            possible_answers = question['answers'].split('@')
            choice_count = len(possible_answers)
            self._block_radio_signals(True)
            for r in range(_MAX_ANSWERS):
                if r >= choice_count:
                    self._choice_options[r].hide()
                    if r==choice_count:
                        self._choice_options[r].setChecked(True)
                else:
                    self._choice_options[r].show()
                    self._choice_options[r].setText(possible_answers[r])
            if user_answer[0] != '':
                self._choice_options[int(user_answer[0])].setChecked(True)
                if user_answer[1] != '':
                    correct_answer_text = self._choice_options[int(correct_answer)].text()
                    self._correct_answer_label2.setText(correct_answer_text)
                    self._correct_answer_label3.setText(user_answer[1])
                else:
                    self._correct_answer_label2.setText('')
                    self._correct_answer_label3.setText('')
            else:
                self._correct_answer_label2.setText('')
                self._correct_answer_label3.setText('')
            self._block_radio_signals(False)
        else:
            self._cryptic_groupbox.show()
            self._multichoice_groupbox.hide()
            self._answer_label.show()
            self._answer_text.show()
            user_answer = self._user_answers[self._question_index]
            self._correct_answer_label2.setText('')
            self._correct_answer_label3.setText('')
            self._answer_text.setText('')
            if user_answer[0] != '':
                self._answer_text.setText(user_answer[0])
                if user_answer[1] !=  '':
                    self._correct_answer_label2.setText(self._correct_answers[self._question_index])
                    self._correct_answer_label3.setText(user_answer[1])
        self._credits_label.setText(self._resources['lblCredits']+':'+question['credits'])
        self.setFixedSize(self._v_layout.sizeHint())
    def _previous_clicked(self):
        if self._question_index==self._question_count:
            self._show_hide_summary_ui(show=False)
        current_question_index = self._question_index
        previous_index = (current_question_index-1)
        if previous_index >= 0:
            self._question_index = previous_index
            self._update_question()
    def _next_clicked(self):
        current_question_index = self._question_index
        next_index = (current_question_index+1)
        if next_index < self._question_count:
            self._question_index = next_index
            self._update_question()
        elif next_index==self._question_count:
            self._question_index = next_index
            self._show_hide_summary_ui(show=True)
            self._update_summary_ui()
    def _close_clicked(self):
        print('closing quiz')
        self.close()            
def _get_quiz_db():
    quiz_db  = {}
    print(quiz_file)
    csv_data = open(quiz_file,"r") 
    with  csv_data:
        reader = csv.reader(csv_data,delimiter='!')
        headers = next(reader)
        #print(headers)
        id = -1
        for row in reader:
            id += 1
            quiz_db[id] = {key.strip(): value.strip() for key, value in zip(headers, row)}
            quiz_db[id]['id'] = id
    csv_data.close()
    return quiz_db
def _get_random_questions(quiz_db,question_count=10):
    q_ids = random.sample(range(len(quiz_db)),question_count)
    questions = []
    for i in q_ids:
        questions.append(quiz_db[i])
    return questions    
def show(question_count=10):
    import sys
    def except_hook(exc_type, exc_value, exc_tb):
        import traceback
        tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        print("Quiz Exception error message:\n", tb)
    sys.excepthook = except_hook

    dialog = QuizUI(question_count=question_count)
    dialog.exec()
if __name__ == "__main__":
    import sys
    def except_hook(exc_type, exc_value, exc_tb):
        import traceback
        tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        print("Quiz Exception error message:\n", tb)
    sys.excepthook = except_hook

    app = QApplication(sys.argv)
    settings.set_language('ta')
    dialog = QuizUI(question_count=5)
    dialog.show()
    sys.exit(app.exec())        
    