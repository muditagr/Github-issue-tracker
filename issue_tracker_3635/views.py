from datetime import datetime, timedelta

import requests
from django.conf import settings
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import generic
import dateutil.parser
from django.contrib import messages



class TrackIssue(generic.TemplateView):
    http_method_name = ('get') # allowed method for this view
    template_name = 'track_gh_issue.html' # serve html with context

    def get_context_data(self, **kwargs):
        context = super(TrackIssue, self).get_context_data(**kwargs)

        # get url of the repository via get parameter
        repo_ulr = self.request.GET.get('repo_url')

        # if only repository url exists
        if repo_ulr:
            repo_name = repo_ulr.split('/')[-1] # get name of the repo
            repo_owner = repo_ulr.split('/')[-2] # get repo's owner

            # construct url of the github issues API
            url = 'https://api.github.com/repos/{}/{}/issues?per_page=100&page=1'.format(
                repo_owner,
                repo_name
            )
            response = requests.get(
                url,
                headers={
                    "Authorization": settings.GITHUB_AUTH_TOKEN,
                    }
            )
            # if response is not success, return with error message
            if response.status_code != 200:
                messages.add_message(self.request, messages.ERROR, 'Invalid URL or repository is private')
                return context

            res = response.json()

            # paginate with 'next' url present in github response
            while 'next' in response.links.keys():
                response=requests.get(
                        response.links['next']['url'],
                        headers={"Authorization": settings.GITHUB_AUTH_TOKEN}
                    )
                res.extend(response.json())

            # github issues api considers pull requests as issue as well, line below ignores pr's
            issues = [r for r in res if not r.get('pull_request')]

            now = timezone.now()

            past_24_hour = now - timedelta(hours=24)

            past_7_day = now - timedelta(days=7)

            # count initialization of issues wrt to time
            total_count = len(issues)
            count_24_hour = 0
            count_7_day = 0
            count_past = 0
            other = 0

            for issue in issues:
                created_time = dateutil.parser.parse(issue.get('created_at'))

                if created_time >= past_24_hour and created_time<= now:
                    count_24_hour+=1
                elif created_time >= past_7_day:
                    count_7_day+=1
                elif created_time < past_7_day:
                    count_past +=1
                else:
                    other+=1

            context['repo_name'] = repo_name
            context['repo_url'] = repo_ulr
            context['total_count'] = total_count
            context['count_24_hour'] = count_24_hour
            context['count_7_day'] = count_7_day
            context['count_past'] = count_past

        return context