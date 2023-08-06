(function ($) {

	"use strict";

	var fullHeight = function () {

		$('.js-fullheight').css('height', $(window).height());
		$(window).resize(function () {
			$('.js-fullheight').css('height', $(window).height());
		});

	};
	fullHeight();

	$('#sidebarCollapse').on('click', function () {
		$('#sidebar').toggleClass('active');
	});

})(jQuery);

function getPreviousMonthNames(numOfMonths) {
	const monthNames = [];
	const currentDate = new Date();
	for (let i = 0; i < numOfMonths; i++) {
		const previousMonth = new Date(currentDate.getFullYear(), currentDate.getMonth() - i - 1, 1);
		console.log(currentDate.getMonth() - i - 1)
		const monthName = previousMonth.toLocaleString('default', { month: 'long' });
		monthNames.push(monthName);
	}
	console.log(monthNames, );
	return monthNames;
}

function setDataForPreviousMonths() {
	const monthlyData = {};
	// Generate a random value between a given range
	function getRandomValue(min, max) {
		return Math.floor(Math.random() * (max - min + 1)) + min;
	}
	const months = getPreviousMonthNames(new Date().getMonth());
	console.log(months, "success")
	month_mi = 'January'
	months.forEach(month => {
		console.log(month, "nonoe")
		// const existingData = JSON.parse(localStorage.getItem(month)) || {};
		const existingData = window.monthlyTransactionsData[month] || {};
			// console.log(existData)
		// Check if expense and income fields exist, and initialize them if not
		console.log("OOSS")
		console.log(existingData)
		// console.log(localStorage.getItem(month))
		if (!existingData.expense) {
			existingData.expense = getRandomValue(200, 500)
		}
		if (!existingData.income) {
			existingData.income = getRandomValue(200, 500)
		}
		monthlyData[month] = existingData;
	});

	// Log the current expense and income values for each month
	months.forEach(month => {
		const { expense, income } = monthlyData[month];
		console.log(`Current expense for ${month}: ${expense}`);
		console.log(`Current income for ${month}: ${income}`);
		localStorage.setItem(month, JSON.stringify(monthlyData[month]));
	});
}