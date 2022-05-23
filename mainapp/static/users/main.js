const html = document.documentElement;
const body = document.body;
const menuLinks = document.querySelectorAll(".admin-menu a");
const collapseBtn = document.querySelector(".admin-menu .collapse-btn");
const toggleMobileMenu = document.querySelector(".toggle-mob-menu");
const switchInput = document.querySelector(".switch input");
const switchLabel = document.querySelector(".switch label");
const switchLabelText = switchLabel.querySelector("span:last-child");
const collapsedClass = "collapsed";
const lightModeClass = "light-mode";

/*TOGGLE HEADER STATE*/
collapseBtn.addEventListener("click", function () {
  body.classList.toggle(collapsedClass);
  this.getAttribute("aria-expanded") == "true"
    ? this.setAttribute("aria-expanded", "false")
    : this.setAttribute("aria-expanded", "true");
  this.getAttribute("aria-label") == "collapse menu"
    ? this.setAttribute("aria-label", "expand menu")
    : this.setAttribute("aria-label", "collapse menu");
});

/*TOGGLE MOBILE MENU*/
toggleMobileMenu.addEventListener("click", function () {
  body.classList.toggle("mob-menu-opened");
  this.getAttribute("aria-expanded") == "true"
    ? this.setAttribute("aria-expanded", "false")
    : this.setAttribute("aria-expanded", "true");
  this.getAttribute("aria-label") == "open menu"
    ? this.setAttribute("aria-label", "close menu")
    : this.setAttribute("aria-label", "open menu");
});

/*SHOW TOOLTIP ON MENU LINK HOVER*/
for (const link of menuLinks) {
  link.addEventListener("mouseenter", function () {
    if (
      body.classList.contains(collapsedClass) &&
      window.matchMedia("(min-width: 768px)").matches
    ) {
      const tooltip = this.querySelector("span").textContent;
      this.setAttribute("title", tooltip);
    } else {
      this.removeAttribute("title");
    }
  });
}

/*TOGGLE LIGHT/DARK MODE*/
if (localStorage.getItem("dark-mode") === "false") {
  html.classList.add(lightModeClass);
  switchInput.checked = false;
  switchLabelText.textContent = "Light";
}

switchInput.addEventListener("input", function () {
  html.classList.toggle(lightModeClass);
  if (html.classList.contains(lightModeClass)) {
    switchLabelText.textContent = "Light";
    localStorage.setItem("dark-mode", "false");
  } else {
    switchLabelText.textContent = "Dark";
    localStorage.setItem("dark-mode", "true");
  }
});

// script for tab steps
    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {

        var href = $(e.target).attr('href');
        var $curr = $(".process-model  a[href='" + href + "']").parent();

        $('.process-model li').removeClass();

        $curr.addClass("active");
        $curr.prevAll().addClass("visited");
    });
// end  script for tab steps



  //deposit button event handler
  const deposit_btn = document.getElementById('deposit-btn');
  deposit_btn.addEventListener('click', function(){

      const depositStringToInt = getInputNumb("deposit-amount");

      updateSpanTest("current-deposit", depositStringToInt);
      updateSpanTest("current-balance", depositStringToInt);

      //setting up the input field blank when clicked
      document.getElementById('deposit-amount').value = "";

  })

    //withdraw button event handler
    const withdraw_btn = document.getElementById('withdraw-btn');
    withdraw_btn.addEventListener('click', function(){
      const withdrawNumb = getInputNumb("withdraw-amount");

      updateSpanTest("current-withdraw", withdrawNumb);
      updateSpanTest("current-balance", -1 * withdrawNumb);
      //setting up the input field blank when clicked
      document.getElementById('withdraw-amount').value = "";
  })

  //function to parse string input to int
  function getInputNumb(idName){
      const amount = document.getElementById(idName).value;
      const amountNumber = parseFloat(amount);
      return amountNumber;
  }

  function updateSpanTest(idName, addedNumber){
      //x1.1 updating balance the same way
      const current = document.getElementById(idName).innerText;
      const currentStringToInt = parseFloat(current);

      const total = currentStringToInt + addedNumber;

      //x1.2 setting this value in balance
      document.getElementById(idName).innerText = total;
  }

  document