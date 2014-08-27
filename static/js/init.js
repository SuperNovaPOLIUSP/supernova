_5grid.ready(function() {

	var _bh = $('html,body');

	// Dropdown Menus (desktop only)
		if (_5grid.isDesktop)
			$('#nav > ul').dropotron({
				offsetY: -20,
				offsetX: -1,
				mode: 'fade',
				noOpenerFade: true
			});

	// Banner slider
		var banner = $('#slider');
		if (banner.length > 0)
		{
			banner.slidertron({
					mode: 'fade',	// Change this to 'slide' to switch back to sliding mode
					seamlessWrap: false,
					viewerSelector: '.viewer',
					speed: 'slow',
					autoFit: true,
					autoFitAspectRatio: (1200 / 635),
					reelSelector: '.viewer .reel',
					slidesSelector: '.viewer .reel .slide',
					advanceDelay: (_5grid.isMobile ? 4500 : 6000),
					speed: 'slow',
					navPreviousSelector: '.previous-button',
					navNextSelector: '.next-button',
					indicatorSelector: '.indicator ul li',
					slideLinkSelector: '.link',
					captionLines:			1,
					captionLineSelector:	'.captionLine',
					slideCaptionSelector:	'.caption'
			});

			if (_5grid.isMobile)
			{
				_5grid.orientationChange(function() {
					banner.trigger('slidertron_reFit');
				});

				_5grid.mobileUINavOpen(function() {
					banner.trigger('slidertron_stopAdvance');
				});
			}
		}
		
	// Portfolio
		var portfolio = $('#portfolio');
		if (portfolio.length > 0)
		{
			var _settings;

			portfolio.rotatorrr({
				titlesSelector: '.titles li',
				slidesSelector: '.category'
			});

			if (_5grid.isMobile)
			{
				portfolio.find('.button-top').click(function(e) {
					_bh.animate({ scrollTop: portfolio.offset().top - 60 }, 800, 'swing');
					return false;
				});

				_settings = {
					usePopupCaption: true,
					overlayOpacity: 0.8,
					useBodyOverflow: false,
					usePopupCloser: false,
					popupPadding: 0,
					windowMargin: 5,
					popupCaptionHeight: 40,
					popupSpeed: 0,
					fadeSpeed: 0
				};
			}
			else
				_settings = {
					usePopupCaption: true,
					overlayOpacity: 0.8,
					useBodyOverflow: false,
					usePopupCloser: false
				};
				
			portfolio.find('.category').each(function() {
				$(this).poptrox(_settings);
			});

		}

});