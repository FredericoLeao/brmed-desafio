var currencyQuotation = null
var filteredQuotation = null

// DatePicker: set default suggested date as '5 days ago'
const elements = document.querySelector('#date-range-container')
const defaultViewDate = new Date()
defaultViewDate.setDate(defaultViewDate.getDate() - 4)
const datepicker = new DateRangePicker(elements, {
    format: 'dd/mm/yyyy',
    maxDate: new Date(),
    defaultViewDate: defaultViewDate,
    language: 'pt-BR'
})

function createChart(data) {
    const chart = Highcharts.chart('chart-container', {
        chart: {
            type: 'line'
        },
        title: {
            text: 'Cotação de moedas'
        },
        xAxis: {
            categories: data.map((_data) => { return _data[0] })
        },
        series: [{
            data: data.map((_data) => { return _data[1] })
        }]
    })
}

function reloadChart() {
    if (!(currencyQuotation.length > 0)) {
        return
    }

    // pick rates data according to selected currency
    selectedCurrency = document.querySelector('#currencySelect').value.toUpperCase()
    filteredQuotation = currencyQuotation.map((data) => {
        return [data.date, data.rates[selectedCurrency]]
    })

    createChart(filteredQuotation)
}

function getCurrencyQuotation() {
    document.querySelector('#error-msg').innerHTML = ''

    const start_date = document.querySelector('#start_date').value
    const end_date = document.querySelector('#end_date').value
    fetch(`/api/rates/?start_date=${start_date}&end_date=${end_date}`)
    .then(function(response) {
        if (response.status == 200) {
            response.json().then((data) => {
                currencyQuotation = data
                reloadChart()
            })
        }
        else {
            response.json().then((data) => {
                if ('msg' in data) {
                    document.querySelector('#error-msg').innerHTML = data.msg
                }
            })
        }
    })
}

const currencySelect = document.querySelector('#currencySelect')
currencySelect.addEventListener('input', (event) => {
    reloadChart()
}, false);