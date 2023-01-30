from .splash import Splash
from requests.exceptions import ReadTimeout


class USPSTrackingService:
    def __init__(self, proxy=False,):
        self.splash = Splash()

    def parse_html(self, html):
        res = {'success': False}

        res['status'] = html.find('.banner-header', first=True).text
        res['desc'] = html.find('.banner-content', first=True).text
        res['value'] = []
        steps = [s for s in html.find('.tb-step') if s.find('p')]
        res['success'] = True if steps else False
        for step in steps:
            step_record = {s.attrs['class'][0].strip('tb-'): s.text.strip().replace('\xa0', ' ') for s in step.find('p')}
            res['value'].insert(0, step_record)
        return res

    def get_tracking_result(self, tracking_number):
        print('=> [USPS] Get Tracking Result:', tracking_number)
        try:
            r = self.splash.session.get(f'https://tools.usps.com/go/TrackConfirmAction?qtc_tLabels1={tracking_number}', timeout=10)
        except ReadTimeout:
            return self.get_tracking_result(tracking_number)

        tracking_html = r.html.find('.track-statusbar', first=True)

        if tracking_html:
            result = self.parse_html(tracking_html)
        else:
            self.splash.update_session_cookies()
            return self.get_tracking_result(tracking_number)

        return result


if __name__ == '__main__':
    service = USPSTrackingService(proxy=False)
    result = service.get_tracking_result('LR016650445CN')
    print(result)

    tracking_numbers = ['LR004178233CN', 'LR004605625CN', 'LR004324951CN', 'LR009975923CN',
                        'LR010654841CN', 'LR008799839CN', 'CY012519328CN', 'LR011995436CN',
                        'LR016452207CN', 'LR016650445CN', 'LR017380047CN', 'LR014890505CN',
                        'LR021365770CN'
                        ]

    for tracking_number in tracking_numbers*5:
        result = service.get_tracking_result(tracking_number)
        print(result)
        print('=' * 50)