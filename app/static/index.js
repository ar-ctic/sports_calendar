const BASE_URL = 'http://localhost:5000'

let startDate = ""
let endDate = ""
const limit = 10
let offset = 0

const fileInput = document.getElementById("file-input")
fileInput.addEventListener("change", async function () {
    /**
     * On fileinput get the file, call 'uploadFile' if file is JSON
     */
    const file = fileInput.files[0]

    const formData = new FormData()
    formData.append("file", file)

    if (file && file.type === "application/json") {
        uploadFile(formData)
    }
})


function dateFormatter(date) {
    /**
     * Formats the date to format: "YYYY-mm-dd"
     * 
     * @param {Object} date - object that contains data about selected date
     * 
     * @returns {string} - formatted date
     */
    let formattedDate = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${(date.getDate()).toString().padStart(2, '0')}`
    return formattedDate
}


document.addEventListener('DOMContentLoaded', function () {

    const display_date = document.getElementById("date-display-text")
    const button_clear_date = document.getElementById("date-display-clear")



    const datePicker = flatpickr("#daterange", {
        mode: "range",
        inline: true,

        onChange: function (selectedDates) {

            if (!selectedDates[0]) return

            let startDate = dateFormatter(selectedDates[0])

            let endDate = ""
            if (selectedDates[1]) {
                endDate = dateFormatter(selectedDates[1])

            }

            display_date.textContent = endDate ? `${startDate} to ${endDate}` : `${startDate}`

        },

        onClose: function (selectedDates) {
            startDate = dateFormatter(selectedDates[0])
            endDate = dateFormatter(selectedDates[1])

        }
    })

    button_clear_date.addEventListener('click', function () {
        display_date.textContent = ""
        datePicker.clear()
        startDate = ""
        endDate = ""
    })

})







function findMatches() {
    /**
     * Find new matches, reset offset and clear "games" div
     */
    offset = 0
    const gamesContainer = document.getElementById('games')
    gamesContainer.innerHTML = ""
    getMatches()
}

function loadMore() {
    /**
     * Load new matches, increment offset by limit
     */
    offset += limit
    getMatches()
}


function setCompetitionSelect(data) {
    /**
     * Sets option in select input for each competition in data
     * 
     * @param {Object} data - Object that contains all available competitions
     * 
     */
    const competitionSelect = document.getElementById("select-competition")

    data.forEach(item => {
        const option = document.createElement('option')

        option.value = item
        option.textContent = item

        competitionSelect.appendChild(option)

    })
}


function setGames(data) {
    /**
     * Adds divs with game details into "games" div, shows or hides "load-more"
     */
    const gamesContainer = document.getElementById('games')
    const loadMoreContainer = document.getElementById('load-more')

    // If length of date is smaller than query limit all data has loaded -> hide "load-more" else show
    if (data.length < limit) {
        loadMoreContainer.style.display = "none"
    } else {
        loadMoreContainer.style.display = "flex"
    }

    function createDetailElement(textContent) {
        /**
         * creates Text Element with game detail
         * 
         * @param {string} textContent - game detail
         * 
         * @returns {Object} detailElement - <p> text element with textContent as textContent
         */
        const detailElement = document.createElement('p')
        detailElement.className = "game-detail"
        detailElement.textContent = textContent === null ? "---" : textContent
        return detailElement
    }

    function getGameDetailSections(game) {
        /**
         * Sorts game data in a list as it will be displayed and slices it into 5 sublists
         * 
         * @param {Object} game - List object with game details
         * 
         * @returns {Object} sections - List of Lists with game details for each div
         */
        const date = new Date(game[3] * 1000).toLocaleString('en-GB', { timeZone: 'UTC' })

        // Reorder list: [Season, Date, Time, Competition, Stage, Status, Stadium, HomeTeam, AwayTeam, Goals-HomeTeam, Goals-AwayTeam]
        const gameDetails = [game[0], date, game[8], game[9], game[1], game[2], game[5], game[6], game[10], game[11]]

        // Define slices for each section
        const sections = [
            gameDetails.slice(0, 2),
            gameDetails.slice(2, 4),
            gameDetails.slice(4, 6),
            gameDetails.slice(6, 8),
            gameDetails.slice(8, 10)
        ]

        return sections
    }

    data.forEach(game => {
        const gameElement = document.createElement('div')
        gameElement.className = "game-container"


        const sections = getGameDetailSections(game)

        // Create a div for each section and add the corresponding details
        sections.forEach(section => {
            const sectionElement = document.createElement('div')
            sectionElement.className = "game-section"
            section.forEach(detail => sectionElement.appendChild(createDetailElement(detail)))
            gameElement.appendChild(sectionElement)
        })

        // Add the structured game element to the games container
        gamesContainer.appendChild(gameElement)
    })




}


function getCheckboxStatus() {
    /**
     * Gets value from status checkboxes
     * 
     * @returns {Object} - values of checkboxes
     * 
     */
    const scheduledCheckbox = document.getElementById("scheduled-checkbox")
    const ongoingCheckbox = document.getElementById("ongoing-checkbox")
    const playedCheckbox = document.getElementById("played-checkbox")

    const selectedValues = []

    if (scheduledCheckbox.checked) {
        selectedValues.push(scheduledCheckbox.value)
    }
    if (ongoingCheckbox.checked) {
        selectedValues.push(ongoingCheckbox.value)
    }
    if (playedCheckbox.checked) {
        selectedValues.push(playedCheckbox.value)
    }

    return selectedValues

}


function getVenueName() {
    /**
     * Gets venue-name value from input
     * 
     * @returns {string | null} - value of input 
     * 
     */
    const venueNameInput = document.getElementById("venue-name")
    const venueName = venueNameInput.value
    const trimmedVenueName = venueName.trim()

    return trimmedVenueName
}


function getTeamName() {
    /**
     * Gets team-name value from input
     * 
     * @returns {string | null} - value of input 
     * 
     */
    const teamNameInput = document.getElementById("team-name")
    const teamName = teamNameInput.value
    const trimmedTeamName = teamName.trim()

    return trimmedTeamName
}


function getCompetitionName() {
    /**
     * Gets competition-name value from select
     * 
     * @returns {string | null} - value of input
     * 
     */
    const competitionNameSelect = document.getElementById("select-competition")
    const competitionName = competitionNameSelect.value
    const trimmedCompetitionName = competitionName.trim()

    return trimmedCompetitionName
}



async function makeRequest(endpoint, options = { method: 'GET' }) {
    /**
    * Sends an HTTP request to specified url with provided options
    *
    * @param {string} endpoint - Endpoint to API
    * @param {object} options - Settings for request, such as method, headers and body. Defaults to {method: 'GET' }
    *
    * @returns {Promise < Object >} - Promise which resolves into JSON response if successful
    *
    */
    const url = `${BASE_URL}${endpoint}`

    try {
        let response = await fetch(url, options)

        if (!response.ok) {
            throw new Error(`HTTP Error! Status: ${response.status}`)
        }

        return response.json()

    } catch (error) {
        console.error(`ERROR ${error}`)
        return { success: false, message: error.message }
    }
}


async function getMatches() {
    /**
    * Calls GET API '/getMatches' which returns all matches based on parameters provided
    *
    */
    const params = {
        "startDate": startDate,
        "endDate": endDate,
        "status": getCheckboxStatus(),
        "venueName": getVenueName(),
        "teamName": getTeamName(),
        "competition": getCompetitionName(),
        "limit": limit,
        "offset": offset
    }

    const options = {
        method: "GET"
    }

    let data = await makeRequest(`/getMatches?startDate=${params.startDate}&endDate=${params.endDate}&status=${params.status}&venueName=${params.venueName}&teamName=${params.teamName}&competition=${params.competition}&limit=${params.limit}&offset=${params.offset}`,
        options)

    setGames(data)
}



async function getCompetitions() {
    /**
    * Calls GET API '/getCompetitions' which returns the names of all competitions
    * Sets options in select element for every competition
    *
    */
    const options = {
        method: 'GET'
    }

    let data = await makeRequest('/getCompetitions', options)

    setCompetitionSelect(data)

}


async function uploadFile(file) {
    /**
    * Calls POST API '/upload' which returns Object if matches were inserted successfully
    *
    */
    const options = {
        method: 'POST',
        body: file
    }

    let data = await makeRequest('/upload', options)
    console.log(data)

}

getCompetitions()
