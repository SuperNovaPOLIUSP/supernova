/*
	Rotatorrr 1.0: Rotates between stuff.
	By n33 | http://n33.co | @nodethirtythree
	Dual licensed under the MIT or GPLv2 license.
	//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	MIT LICENSE:
	Copyright (c) 2012 n33, http://n33.co
	Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation
	files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use,
	copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
	Software is furnished to do so, subject to the following conditions:
	The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
	OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
	HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
	FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
	//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	GPLv2 LICENSE:
	Copyright (c) 2012 n33, http://n33.co
	This program is free software: you can redistribute it and/or modify it	under the terms of the GNU General Public License as
	published by the Free Software Foundation, either version 2 of the License, or (at your option) any later version. This program is
	distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY 
	or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received a copy of
	the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>. 
	//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
*/

(function(jQuery) {

	jQuery.fn.disableSelection_rotatorrr = function() { return jQuery(this).css('user-select', 'none').css('-khtml-user-select', 'none').css('-moz-user-select', 'none').css('-o-user-select', 'none').css('-webkit-user-select', 'none'); }

	jQuery.fn.rotatorrr = function(options) {
		var settings = jQuery.extend({
			selectorParent:		jQuery(this)
		}, options);
		
		return jQuery.rotatorrr(settings);
	}

	jQuery.rotatorrr = function(options) {

		// Settings
		
			var settings = jQuery.extend({
			
				selectorParent:						null,						// If a jQuery object, all selectors will be restricted to its scope. Otherwise, all selectors will be global.
				
				// Selectors
				
					titlesSelector:					null,						// Titles selector
					slidesSelector:					null,						// Slides selector
					navNextSelector:				null,						// 'Next' selector
					navPreviousSelector:			null,						// 'Previous' selector
					navFirstSelector:				null,						// 'First' selector
					navLastSelector:				null,						// 'Last' selector
					navStopAdvanceSelector:			null,						// 'Stop Advance' selector
					navPlayAdvanceSelector:			null,						// 'Play Advance' selector

				// General settings

					speed:							'fast',						// Transition speed (0 for instant, 'slow', 'fast', or a custom duration in ms)
					advanceDelay:					0,							// Time to wait (in ms) before automatically advancing to the next slide (0 disables advancement entirely)
					advanceResume:					0,							// Time to wait (in ms) before resuming advancement after a user interrupts it by manually navigating (0 disables resuming advancement)
					advanceNavActiveClass:			'active',					// Active advancement navigation class
					titlesActiveClass:				'active',					// Active title class
					initialSlideClass:				'initial',					// Initial slide class
					useHash:						true,						// If true, uses the URL hash value to figure out the initial slide (overriding the "initial" class)
					replaceLocation:				true						// (experimental)

			}, options);
			
		// Variables

			// Operational stuff
		
				var isConfigured = true,
					isLocked = false,
					isAdvancing = false,
					list = new Array(),
					currentIndex = false,
					initialIndex = 0,
					timeoutID;

				var _isTouch = !!('ontouchstart' in window), _eventType = (_isTouch ? 'touchend' : 'click');

			// jQuery objects

				var __slides,
					__viewer,
					__navFirst,
					__navLast,
					__navNext,
					__navPrevious,
					__navStopAdvance,
					__navPlayAdvance;

		// Functions
			
			function getElement(selector, required)
			{
				var x;
				
				try
				{
					if (selector == null)
						throw 'is undefined';
			
					if (settings.selectorParent)
						x = settings.selectorParent.find(selector);
					else
						x = jQuery(selector);
					
					if (x.length == 0)
						throw 'does not exist';
					
					return x;
				}
				catch (error)
				{
					if (required == true)
					{
						alert('Error: Required selector "' + selector + '" ' + error + '.');
						isConfigured = false;
					}
				}
				
				return null;
			}

			function advance()
			{
				if (settings.advanceDelay == 0)
					return;
			
				if (!isLocked)
					nextSlide();

				timeoutID = window.setTimeout(advance, settings.advanceDelay);
			}

			function initializeAdvance()
			{
				if (settings.advanceDelay == 0)
					return;

				if (__navPlayAdvance)
					__navPlayAdvance.addClass(settings.advanceNavActiveClass);
				
				if (__navStopAdvance)
					__navStopAdvance.removeClass(settings.advanceNavActiveClass);

				isAdvancing = true;
				timeoutID = window.setTimeout(advance, settings.advanceDelay);
			}
			
			function interruptAdvance()
			{
				if (!isAdvancing)
					return;

				if (settings.advanceDelay == 0)
					return;

				window.clearTimeout(timeoutID);

				if (settings.advanceResume == 0)
					return;

				timeoutID = window.setTimeout(advance, settings.advanceResume);
			}
			
			function stopAdvance()
			{
				if (settings.advanceDelay == 0)
					return;

				if (!isAdvancing)
					return;
			
				isAdvancing = false;
				window.clearTimeout(timeoutID);
			}
			
			function playAdvance(skip)
			{
				if (settings.advanceDelay == 0)
					return;

				if (isAdvancing)
					return;

				isAdvancing = true;

				if (skip)
					timeoutID = window.setTimeout(advance, settings.advanceDelay);
				else
					advance();
			}
			
			function firstSlide()
			{
				switchSlide(0);
			}
			
			function lastSlide()
			{
				switchSlide(list.length - 1);
			}

			function nextSlide()
			{
				if (currentIndex < list.length - 1)
					switchSlide(currentIndex + 1);
				else
					switchSlide(0);
			}
			
			function previousSlide()
			{
				if (currentIndex > 0)
					switchSlide(currentIndex - 1);
				else
					switchSlide(list.length - 1);
			}

			function switchSlide(index)
			{
				// Check locking status (so another switch can't be initiated while another is in progress)

				if (isLocked)
					return false;
				
				if (currentIndex !== false
				&&	currentIndex == index)
					return true;
				
				isLocked = true;

				if (currentIndex === false)
				{
					currentIndex = index;
					list[index].object.show();
					list[index].title.addClass(settings.titlesActiveClass);
					isLocked = false;
				}
				else
				{
					list[currentIndex].title.removeClass(settings.titlesActiveClass);
					list[index].title.addClass(settings.titlesActiveClass);

					list[currentIndex].object.fadeOut(settings.speed, function() {
						list[index].object.fadeIn(settings.speed, function() {
							currentIndex = index;
							isLocked = false;
						});
					});
				}
			}

			function initialize()
			{
				// Titles, slides

					__titles = getElement(settings.titlesSelector, true);
					__slides = getElement(settings.slidesSelector, true);

					if (__titles.size() != __slides.size())
						alert('Number of titles and slides don\'t match. Aborting.');

				// Navigation

					__navFirst = getElement(settings.navFirstSelector);
					__navLast = getElement(settings.navLastSelector);
					__navNext = getElement(settings.navNextSelector);
					__navPrevious = getElement(settings.navPreviousSelector);
					__navStopAdvance = getElement(settings.navStopAdvanceSelector);
					__navPlayAdvance = getElement(settings.navPlayAdvanceSelector);

				// Check configuration status
				
					if (isConfigured == false)
					{
						alert('Error: One or more configuration errors detected. Aborting.');
						return;
					}

				// Set up

					// Slides
				
						var cx = 0, length = __slides.length;

						__slides.hide();
				
						__slides.each(function(index) {

							var y = jQuery(this);

							list[index] = {
								object:		y
							};
						});

					// Titles
					
						__titles.disableSelection_rotatorrr();
					
						__titles.each(function(index) {
						
							var y = jQuery(this);
							
							if (y.hasClass(settings.initialSlideClass))
								initialIndex = index;
							
							list[index].title = y;
							
							if (y.attr('href') && y.attr('href')[0] == '#')
							{
								list[index].name = y.attr('href').substring(1);
								jQuery('a[name="' + list[index].name + '"]').remove();
								y.click(function(e) {
									e.preventDefault();
									if (settings.replaceLocation)
										window.location.replace('#' + list[index].name);
								});
							}

							y.bind(_eventType, function(event) {
								if (isLocked)
									return false;

								if (isAdvancing)
									interruptAdvance();
								
								event.preventDefault();

								switchSlide(index);
							});
							
							if (_eventType != 'click')
								y.click(function(e) { e.preventDefault(); });

						});
						
					// Navigation

						if (__navFirst)
							__navFirst.click(function(event) {
								event.preventDefault();

								if (isLocked)
									return false;

								if (isAdvancing)
									interruptAdvance();
								
								firstSlide();
							});

						if (__navLast)
							__navLast.click(function(event) {
								event.preventDefault();

								if (isLocked)
									return false;

								if (isAdvancing)
									interruptAdvance();

								lastSlide();
							});

						if (__navNext)
							__navNext.click(function(event) {
								event.preventDefault();

								if (isLocked)
									return false;

								if (isAdvancing)
									interruptAdvance();

								nextSlide();
							});

						if (__navPrevious)
							__navPrevious.click(function(event) {
								event.preventDefault();

								if (isLocked)
									return false;
							
								if (isAdvancing)
									interruptAdvance();

								previousSlide();
							});

						if (__navStopAdvance)
							__navStopAdvance.click(function(event) {
								event.preventDefault();

								if (isLocked)
									return false;

								if (!isAdvancing)
									return false;

								__navStopAdvance.addClass(settings.advanceNavActiveClass);
								
								if (__navPlayAdvance)
									__navPlayAdvance.removeClass(settings.advanceNavActiveClass);

								stopAdvance();
							});

						if (__navPlayAdvance)
							__navPlayAdvance.click(function(event) {
								event.preventDefault();

								if (isLocked)
									return false;
									
								if (isAdvancing)
									return false;

								__navPlayAdvance.addClass(settings.advanceNavActiveClass);
								
								if (__navStopAdvance)
									__navStopAdvance.removeClass(settings.advanceNavActiveClass);

								playAdvance();
							});

					// Initial

						if (settings.useHash)
						{
							var tmp = window.location.hash.substring(1);

							if (tmp)
							{
								for (index in list)
								{
									if (list[index].name == tmp)
									{
										initialIndex = index;
										window.scrollTo(0, 0);
										break;
									}
								}
							}
						}

			}

			// Ready

				jQuery().ready(function() {
					initialize();
					initializeAdvance();
					switchSlide(initialIndex);
				});
	};

})(jQuery);