// var headingBox = document.getElementsByClassName('heading')[0];
// var heading = document.getElementsByClassName('headingH2')[0];

// if (heading && headingBox) {
//     // Accessing height using clientHeight property
//     var headingHeight = heading.clientHeight;
//     var headingBoxHeight = headingBox.clientHeight;
//     console.log("Height of headingH2:", headingHeight);
//     console.log("Height of heading:", headingBoxHeight);

//     // Comparing heights
//     var headingH2Elements = document.getElementsByClassName('headingH2');
//     for (var i = 0; i < headingH2Elements.length; i++) {
//         var currentHeadingH2 = headingH2Elements[i];
//         var currentHeadingH2Height = currentHeadingH2.clientHeight;
//         if (currentHeadingH2Height > headingBoxHeight) {
//             console.log('...');
//         }
//     }
// }
// var headingH2Elements = document.getElementsByClassName('headingH2');
//     for (var i = 0; i < headingH2Elements.length; i++) {
//         var currentHeadingH2 = headingH2Elements[i];
//         var currentHeadingH2Height = currentHeadingH2.clientHeight;
//         if (currentHeadingH2Height > headingBoxHeight) {
//             console.log('...');
//         }
//     }

// document.addEventListener("DOMContentLoaded", function() {
//     var headingElements = document.querySelectorAll('.heading');
//     i = 0
//     headingElements.forEach(function(element) {
//         var totalHeight = element.clientHeight;
//         var h2Element = element.querySelector('h2');
//         if( totalHeight > h2Element.clientHeight) {
//             var moreDiv = element.nextElementSibling.querySelector('.more');
//             if (moreDiv) {
//                 moreDiv.style.display = "block";
//             }
//             console.log('...'); 
//         }
//         i++;
//         // if (h2Element) {
//         //     totalHeight += h2Element.clientHeight;
//         // }
//         // console.log(totalHeight);
//     });
// });

// document.addEventListener("DOMContentLoaded", function() {
//     var headingElements = document.querySelectorAll('.heading');
//     headingElements.forEach(function(element) {
//         console.log(element.clientHeight);
//     });
// });



document.addEventListener("DOMContentLoaded", function() {
    var blogCards = document.querySelectorAll('.blog_card');
    blogCards.forEach(function(card) {
        var heading = card.querySelector('.heading');
        var headingH2 = card.querySelector('.headingH2');
        var moreDiv = card.querySelector('.more');
        if (headingH2.clientHeight > heading.clientHeight+10) {
            moreDiv.style.opacity = "1";
        }
    });
});
