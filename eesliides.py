# -*- coding: UTF-8 -*-

from tkinter import *
from tkinter import (ttk, filedialog)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import csv
from collections import Counter
from tkinter import messagebox
import numpy as np
import analysation

filepath = ""
initialdir = "/"

# Function for finding the duration at the time when the event occurred
def time_after_start(event_time, start_time):
    return (event_time - start_time).total_seconds() / 60.0

# Presentation of overall analysation of log file
def present_overall_analysation(file_analysation):
    # Start and time of analysation
    start_time = file_analysation['start_time'][0]
    end_time = file_analysation['end_time'][0]

    # Start time label
    start_time_lbl = Label(page1, text="Ülesannete lahendamise algusaeg: " + str(start_time))
    start_time_lbl.grid(column=0, row=0, sticky="wn")

    # End time label
    end_time_lbl = Label(page1, text="Ülesannete lahendamise lõppaeg: " + str(end_time))
    end_time_lbl.grid(column=0, row=1, sticky="wn")

    # Duration label
    duration_lbl = Label(page1, text="Ülesannete lahendamise aeg: " + str(end_time - start_time))
    duration_lbl.grid(column=0, row=2, sticky="wn")

    # Amount of errors label
    error_lbl = Label(page1, text="Vigade arv: " + str(len(file_analysation['error_type'])))
    error_lbl.grid(column=0, row=3, sticky="wn")

    # Label to show number of program runnings
    running_lbl = Label(page1, text="Käivitamiste kordade arv: " + str(len(file_analysation['running'])))
    running_lbl.grid(column=0, row=4, sticky="wn")

    # Check to see if program running resulted in error
    error_after_running = 0
    for value in file_analysation['running_results_in_error']:
        if value:
            error_after_running += 1

    # Label that shows runnings that resulted in error
    error_after_running_lbl = Label(page1, text="Käivitamiste kordade arv, mis lõppevad veateatega: " + str(error_after_running))
    error_after_running_lbl.grid(column=0, row=5, sticky="wn")

    # Label that shows pasted texts that were longer than n characters
    pasted_lbl = Label(page1, text="Rohkem kui " + spin.get() + " tähemärki pikkade tekstilõikude kleepimiste arv: " + str(len(file_analysation['pasted_text'])))
    pasted_lbl.grid(column=0, row=6, sticky="wn")

# Function for plotting the pie chart of errors
def plot_pie_chart(errors):
    labels = []
    values = []
    error_counter = Counter()

    # Finding the errors amount
    for error in errors:
        error_counter[error] += 1

    # Labels of error types and the amount of every error type that occurred
    for elem in error_counter:
        labels.append(elem)
        values.append(error_counter[elem])

    actual_figure = plt.figure(figsize=(8, 6))
    actual_figure.suptitle("Veatüübid", fontsize=15)

    # Plotting pie chart
    plt.pie(values, labels=labels, autopct=lambda p: '{:.0f}'.format(p * sum(values) / 100), shadow=True)

    # Showing pie chart in GUI
    canvas = FigureCanvasTkAgg(actual_figure, page2)
    canvas.get_tk_widget().grid(row=0, column=0)
    canvas.draw()

# Function for plotting the event plot
def event_plot(running, running_results_in_error, start_time):
    positions = [[], []]

    # Separating the code runnings that resulted in error and those that didn't
    for i in range(len(running)):
        if running_results_in_error[i]:
            positions[1].append(time_after_start(running[i], start_time))
        else:
            positions[0].append(time_after_start(running[i], start_time))

    colors1 = np.array([[0, 1, 0],
                        [1, 0, 0]])

    lineoffsets = ([1,1])

    event_figure = plt.figure(figsize=(8, 6))
    event_figure.suptitle("Käivitamised", fontsize=15)

    # Customizing the ticks frequency
    x = [0]
    if len(positions[0]) > 0 and len(positions[1]) > 0:
        maximum = max(map(max, positions))
    elif len(positions[0]) > 0:
        maximum = max(positions[0])
    elif len(positions[1]) > 0:
        maximum = max(positions[1])
    min = 0
    while min < maximum:
        min += 5
        x.append(min)

    # Plotting event plot
    plt.eventplot(positions, colors=colors1, lineoffsets=lineoffsets)
    plt.ylim((0.5, 2))
    plt.xticks(x)

    # Adding legends
    ax = plt.gca()
    ax.axes.yaxis.set_visible(False)
    ax.legend(['Veateateta', 'Veateatega'])
    ax.set_xlabel('Minutid pärast alustamist')

    # Showing event plot in the GUI
    canvas = FigureCanvasTkAgg(event_figure, page3)
    canvas.get_tk_widget().grid(row=0, column=0)
    canvas.draw()

# Function for making table
def make_pasting_table(pasted_text, pasted_text_time):
    page4.grid_columnconfigure(0, weight=1)
    page4.grid_rowconfigure(0, weight=1)

    canvas = Canvas(page4)
    canvas.grid(row=0, column=0, sticky="nswe")

    frame = Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")
    frame._widgets = []

    # Number of rows
    numbers = ["No"]
    for i in range(len(pasted_text)):
        numbers.append(str(i+1))

    pasted_text_time_info = ["Ajahetk"] + pasted_text_time
    pasted_text_info = ["Kleebitud tekst"] + pasted_text

    data = [numbers, pasted_text_time_info, pasted_text_info]

    # Adding rows with all the data
    for row in range(len(numbers)):
        current_row = []
        for column in range(len(data)):
            label = Label(frame, text=data[column][row], borderwidth=0)
            label.grid(row=row, column=column, sticky="nw", padx=3, pady=5)
            current_row.append(label)
        frame._widgets.append(current_row)

    # Adding scrollbar
    vsb = Scrollbar(page4, orient="vertical", command=canvas.yview)
    vsb.grid(row=0, column=1, sticky='ns')
    canvas.configure(yscrollcommand=vsb.set)
    canvas.configure(scrollregion=canvas.bbox("all"))

    # Connecting canvas movement to scrollbar
    frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure(2, weight=1)

# Function for making table
def make_error_table(error_time, error_type, error_message):
    page5.grid_columnconfigure(0, weight=1)
    page5.grid_rowconfigure(0, weight=1)

    canvas = Canvas(page5)
    canvas.grid(row=0, column=0, sticky="nswe")

    frame = Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")
    frame._widgets = []

    # Number of rows
    numbers = ["No"]
    for i in range(len(error_time)):
        numbers.append(str(i+1))

    error_time_info = ["Ajahetk"] + error_time
    error_type_info = ["Tüüp"] + error_type
    error_message_info = ["Veateade"] + error_message

    data = [numbers, error_time_info, error_type_info, error_message_info]

    # Adding rows with all the data
    for row in range(len(numbers)):
        current_row = []
        for column in range(len(data)):
            label = Label(frame, text=data[column][row], borderwidth=0)
            label.grid(row=row, column=column, sticky="nw", padx=3, pady=5)
            current_row.append(label)
        frame._widgets.append(current_row)

    # Adding scrollbar
    vsb = Scrollbar(page5, orient="vertical", command=canvas.yview)
    vsb.grid(row=0, column=1, sticky='ns')
    canvas.configure(yscrollcommand=vsb.set)
    canvas.configure(scrollregion=canvas.bbox("all"))

    # Connecting canvas movement to scrollbar
    frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure(2, weight=1)

# Function for making csv file with specific data
def make_csv(filename, type, data, labels):
    with open(filename[:-4] + "_" + type + ".csv", "w+", newline="") as data_file:
        data_file_writer = csv.writer(data_file, delimiter=",")
        data_file_writer.writerow(labels)

        # Write data into csv file
        for i in range(len(data[0])-1):
            row = []
            for d in data:
                row += [d[i]]
            data_file_writer.writerow(row)

# Function for making csv files
def make_csvs(filename, file_analysation):

    # making csv with pasted text data
    make_csv(filename, "pasting", [file_analysation['pasted_text_time'], file_analysation['pasted_text']], ["pasted_text_time", "pasted_text"])

    # making csv with errors data
    make_csv(filename, "errors", [file_analysation['error_time'], file_analysation['error_type'], file_analysation['error_message']], ["error_time", "error_type", "error_message"])

    # making csv with runnings data
    make_csv(filename, "runnings", [file_analysation['running'], file_analysation['running_results_in_error']], ["running", "running_results_in_error"])

    # Show information about generated files
    messagebox.showinfo("CSV-failid", "CSV-failid salvestatud kausta " + initialdir)

#Function for log file analysation
def file_analysis():
    global filepath

    # if file and at least one analysation type is chosen then do analysation
    if (chk_csv_var.get() != 0 or chk_graphic_var.get() != 0) and filepath != "":
        # do file analysation
        file_analysation = analysation.analysation(filepath, int(spin.get()))

        # if file analysation wasn't a success because of the logfile then show message about it
        if not file_analysation:
            filename = filepath.rsplit("/", 1)[1]
            messagebox.showinfo("Vigane fail", "Logifail " + filename + " on vigane ja analüüsi ei saa teha.")
        # file analysation was a success
        else:
            # make all csv files
            if chk_csv_var.get() == 1:
                make_csvs(filepath, file_analysation)
            # make all subpages
            if chk_graphic_var.get() == 1:
                plot_pie_chart(file_analysation['error_type'])
                make_pasting_table(file_analysation['pasted_text'], file_analysation['pasted_text_time'])
                make_error_table(file_analysation['error_time'], file_analysation['error_type'], file_analysation['error_message'])
                if len(file_analysation['running']) > 0:
                    event_plot(file_analysation['running'], file_analysation['running_results_in_error'], file_analysation['start_time'][0])
                present_overall_analysation(file_analysation)

# function for opening a file
def file_dialog():
    global filepath
    global initialdir
    if chk_csv_var.get() != 0 or chk_graphic_var.get() != 0:
        chosen_filepath = filedialog.askopenfilename(initialdir=initialdir, title="Vali fail", filetypes=(("Text File", "*.txt"),))
        # Check if user actually chose some file
        if chosen_filepath != "":
            filepath = chosen_filepath
            initialdir, filename = filepath.rsplit("/", 1)
            lbl = Label(lbl_frame, text=filename)
            lbl.grid(column=0, row=1, sticky="e")

# GUI

# window
window = Tk()
window.title("Thonny logifailide analüsaator")
window.geometry('800x750')
window.resizable(False, False)

start_frame = Frame(window, bg="lightgrey")
graph_frame = Frame(window)

window.grid_rowconfigure(0, weight=0)
window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)

start_frame.grid(row=0, sticky="nwe")
start_frame.grid_columnconfigure(0, weight=1)
start_frame.grid_columnconfigure(1, weight=1)

graph_frame.grid(row=1, sticky="wn")

nb = ttk.Notebook(graph_frame)
nb.grid(row=0, column=0)

page1 = Frame(nb)
page1.grid_columnconfigure(0, weight=1)
nb.add(page1, text="Üldinfo")

page2 = Frame(nb)
nb.add(page2, text="Veatüübid")

page3 = Frame(nb)
nb.add(page3, text="Käivitamised")

page4 = Frame(nb)
nb.add(page4, text="Kleebitud tekstid")

page5 = Frame(nb)
nb.add(page5, text="Veateated")

chk_csv_var = IntVar()
chk_csv = Checkbutton(start_frame, text='CSV-failid', variable=chk_csv_var, bg="lightgrey")
chk_csv.grid(column=0, row=0, padx=5, pady=5, sticky="e")

chk_graphic_var = IntVar()
chk_graphic = Checkbutton(start_frame, text='Analüüs graafilises liideses', variable=chk_graphic_var, bg="lightgrey")
chk_graphic.grid(column=1, row=0, padx=5, pady=5, sticky="w")
chk_graphic.select()

pasted_frame = Frame(start_frame, bg="lightgrey")
pasted_frame.grid(row=1, columnspan=2)
pasted_frame.grid_columnconfigure(0, weight=1)
pasted_frame.grid_columnconfigure(1, weight=1)

lbl = Label(pasted_frame, text="Minimaalne kleebitud teksti pikkus: ", bg="lightgrey")
lbl.grid(column=0, row=0, sticky="e", pady=5)

spin = Spinbox(pasted_frame, from_=0, to=5000, width=5)
spin.grid(column=1, row=0, sticky="w", pady=5)

button = ttk.Button(start_frame, width=30, text="Vali logifail (.txt)", command=file_dialog)
button.grid(row=2, columnspan=2, padx=5, pady=2)

button = ttk.Button(start_frame, width=30, text="Tee analüüs", command=file_analysis)
button.grid(row=3, columnspan=2, padx=5, pady=2)

lbl_frame = Frame(start_frame)
lbl_frame.grid(row=2, column=1)

window.mainloop()
