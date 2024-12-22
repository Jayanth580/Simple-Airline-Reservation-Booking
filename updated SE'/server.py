from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for flash messages

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
     {
        "flightNumber": "AI404",
        "departureCity": "Bengaluru",
        "arrivalCity": "Delhi",
        "departureTime": "11:00",
        "arrivalTime": "01:00",  # Corrected arrival time format
        "availableBusinessSeats": 10,
        "availableEconomySeats": 10,
    },
     {
        "flightNumber": "AI505",
        "departureCity": "Hyderabad",
        "arrivalCity": "Pune",
        "departureTime": "08:00",
        "arrivalTime": "10:00",
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
        name = request.form.get('name')
        age_str = request.form.get('age')
        flightNumber = request.form.get('flightNumber')
        seatClass = request.form.get('seatClass')

        # Validate inputs
        if not name or not age_str or not flightNumber or not seatClass:
            flash('All fields are required!')
            return redirect(url_for('book_seat'))

        if not age_str.isdigit():
            flash('Age must be a number.')
            return redirect(url_for('book_seat'))

        age = int(age_str)
        flight = next((f for f in flights if f["flightNumber"] == flightNumber), None)

        if flight:
            if seatClass == 'B' and flight['availableBusinessSeats'] > 0:
                seatNumber = 11 - flight['availableBusinessSeats']
                flight['availableBusinessSeats'] -= 1
            elif seatClass == 'E' and flight['availableEconomySeats'] > 0:
                seatNumber = 11 - flight['availableEconomySeats']
                flight['availableEconomySeats'] -= 1
            else:
                flash('No available seats in the specified class.')
                return redirect(url_for('book_seat'))

            passenger = {
                "name": name,
                "age": age,
                "seatClass": seatClass,
                "seatNumber": seatNumber,
                "flightNumber": flightNumber
            }
            passengers.append(passenger)
            flash('Ticket booked successfully!')
            return redirect(url_for('display_ticket', flightNumber=flightNumber, seatNumber=seatNumber))
        else:
            flash('Flight not found.')

    return render_template('book_seat.html', flights=flights)

@app.route('/display_ticket')
def display_ticket():
    flightNumber = request.args.get('flightNumber')
    seatNumber_str = request.args.get('seatNumber')

    if seatNumber_str and seatNumber_str.isdigit():
        seatNumber = int(seatNumber_str)
    else:
        seatNumber = None

    passenger = next((p for p in passengers if p["flightNumber"] == flightNumber and p["seatNumber"] == seatNumber), None)
    flight = next((f for f in flights if f["flightNumber"] == flightNumber), None)

    if not passenger:
        return "Passenger not found", 404
    if not flight:
        return "Flight not found", 404

    return render_template('display_ticket.html', passenger=passenger, flight=flight)

@app.route('/delete_ticket', methods=['GET', 'POST'])
def delete_ticket():
    if request.method == 'POST':
        flightNumber = request.form.get('flightNumber')
        seatNumber_str = request.form.get('seatNumber')

        if not seatNumber_str or not flightNumber:
            flash('Flight number and seat number are required.')
            return redirect(url_for('delete_ticket'))

        if not seatNumber_str.isdigit():
            flash('Seat number must be a number.')
            return redirect(url_for('delete_ticket'))

        seatNumber = int(seatNumber_str)
        passenger = next((p for p in passengers if p["flightNumber"] == flightNumber and p["seatNumber"] == seatNumber), None)
        if passenger:
            passengers.remove(passenger)

            flight = next((f for f in flights if f["flightNumber"] == flightNumber), None)
            if flight:
                if passenger['seatClass'] == 'B':
                    flight['availableBusinessSeats'] += 1
                elif passenger['seatClass'] == 'E':
                    flight['availableEconomySeats'] += 1
                flash('Ticket deleted successfully.')
            else:
                flash('Flight not found.')
        else:
            flash('Ticket not found.')

        return redirect(url_for('index'))

    return render_template('delete_ticket.html', flights=flights)

@app.route('/view_tickets')
def view_tickets():
    return render_template('view_tickets.html', passengers=passengers, flights=flights)

if __name__ == '__main__':
    app.run(debug=True)
