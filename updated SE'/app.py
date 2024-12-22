from flask import Flask, render_template, request, redirect, url_for, flash
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # for flash messages

# Sample data
flights = [
    {
        "flightNumber": "AI101",
        "departureCity": "Chennai",
        "arrivalCity": "Sri Lanka",
        "departureTime": "09:00",
        "arrivalTime": "12:00",
        "availableBusinessSeats": 10,
        "availableEconomySeats": 10,
    },
    {
        "flightNumber": "AI202",
        "departureCity": "Bengaluru",
        "arrivalCity": "Mumbai",
        "departureTime": "13:00",
        "arrivalTime": "16:00",
        "availableBusinessSeats": 10,
        "availableEconomySeats": 10,
    },
    {
        "flightNumber": "AI303",
        "departureCity": "Gujarat",
        "arrivalCity": "Delhi",
        "departureTime": "18:00",
        "arrivalTime": "21:00",
        "availableBusinessSeats": 10,
        "availableEconomySeats": 10,
    },
]

passengers = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/display_flights')
def display_flights():
    return render_template('display_flights.html', flights=flights)

@app.route('/book_seat', methods=['GET', 'POST'])
def book_seat():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        flightNumber = request.form['flightNumber']
        seatClass = request.form['seatClass']

        # Find the flight
        flight = next((f for f in flights if f["flightNumber"] == flightNumber), None)
        if flight:
            if seatClass == 'B' and flight['availableBusinessSeats'] > 0:
                seatNumber = 10 - flight['availableBusinessSeats'] + 1
                flight['availableBusinessSeats'] -= 1
            elif seatClass == 'E' and flight['availableEconomySeats'] > 0:
                seatNumber = 10 - flight['availableEconomySeats'] + 1
                flight['availableEconomySeats'] -= 1
            else:
                flash('No available seats in the specified class.')
                return redirect(url_for('book_seat'))

            passenger = {
                "name": name,
                "age": int(age),
                "seatClass": seatClass,
                "seatNumber": seatNumber,
                "flightNumber": flightNumber
            }
            passengers.append(passenger)
            flash('Ticket booked successfully!')
            return redirect(url_for('display_ticket', flightNumber=flightNumber, seatNumber=seatNumber))

    return render_template('book_seat.html', flights=flights)

@app.route('/display_ticket')
def display_ticket():
    flightNumber = request.args.get('flightNumber')
    seatNumber_str = request.args.get('seatNumber')
    
    # Check if seatNumber_str is not None and is convertible to int
    if seatNumber_str is not None and seatNumber_str.isdigit():
        seatNumber = int(seatNumber_str)
    else:
        seatNumber = None

    passenger = next((p for p in passengers if p["flightNumber"] == flightNumber and p["seatNumber"] == seatNumber), None)
    flight = next((f for f in flights if f["flightNumber"] == flightNumber), None)

    return render_template('display_ticket.html', passenger=passenger, flight=flight)


@app.route('/delete_ticket', methods=['GET', 'POST'])
def delete_ticket():
    if request.method == 'POST':
        flightNumber = request.form['flightNumber']
        seatNumber = int(request.form['seatNumber'])

        passenger = next((p for p in passengers if p["flightNumber"] == flightNumber and p["seatNumber"] == seatNumber), None)
        if passenger:
            passengers.remove(passenger)

            flight = next((f for f in flights if f["flightNumber"] == flightNumber), None)
            if passenger['seatClass'] == 'B':
                flight['availableBusinessSeats'] += 1
            elif passenger['seatClass'] == 'E':
                flight['availableEconomySeats'] += 1

            flash('Ticket deleted successfully.')
            return redirect(url_for('index'))
        else:
            flash('Ticket not found.')
    
    return render_template('delete_ticket.html', flights=flights)

if __name__ == '__main__':
    app.run(debug=True)
