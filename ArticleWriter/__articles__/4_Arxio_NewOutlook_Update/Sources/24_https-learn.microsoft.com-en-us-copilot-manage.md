<!-- Source: https://learn.microsoft.com/en-us/copilot/manage -->

Table of contents Exit editor mode

Ask LearnAsk LearnFocus mode

Table of contents[Read in English](https://learn.microsoft.com/en-us/copilot/manage)Add to CollectionsAdd to plan[Edit](https://learn.microsoft.com/en-us/copilot/manage)

* * *

#### Share via

[Facebook](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fcopilot%2Fmanage%3FWT.mc_id%3Dfacebook) [x.com](https://twitter.com/intent/tweet?original_referer=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fcopilot%2Fmanage%3FWT.mc_id%3Dtwitter&tw_p=tweetbutton&url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fcopilot%2Fmanage%3FWT.mc_id%3Dtwitter) [LinkedIn](https://www.linkedin.com/feed/?shareActive=true&text=%0A%0D%0Ahttps%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fcopilot%2Fmanage%3FWT.mc_id%3Dlinkedin) [Email](mailto:?subject=%5BShared%20Article%5D%20Manage%20Microsoft%20365%20Copilot%20Chat%20%7C%20Microsoft%20Learn&body=%0A%0D%0Ahttps%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fcopilot%2Fmanage%3FWT.mc_id%3Demail)

* * *

Copy MarkdownPrint

* * *

Note

Access to this page requires authorization. You can try [signing in](https://learn.microsoft.com/en-us/copilot/manage#) or changing directories.


Access to this page requires authorization. You can try changing directories.


# Manage Microsoft 365 Copilot Chat

Feedback

Summarize this article for me


[Section titled: Microsoft 365 Copilot Chat eligibility](https://learn.microsoft.com/en-us/copilot/manage#microsoft-365--chat-eligibility)

## Microsoft 365 Copilot Chat eligibility

Copilot Chat is available at no additional cost for Entra account users with one of the following licenses:

- Microsoft 365 A1/A3/A5 (including MA3/MA5 for students, MA3/MA5 for faculty, and MA3/MA5 student-use benefit)
- Microsoft 365 Business Basic/Business Standard/Business Premium
- Microsoft 365 E3/E5
- Microsoft 365 F1/F3
- Microsoft 365 G3/G5
- Microsoft Teams/Teams Enterprise/Teams Essentials/Teams Rooms
- Office 365 A1/A1 Plus/A3/A5
- Office 365 E1/E1 Plus/E3/E5
- Office 365 F3
- Office 365 G1/G3/G5

License versions above that are designated "(no Teams)" and "EEA (no Teams)" are also included.

Copilot Chat is available for students aged 13 and older. To help ensure appropriate access, admins must take additional steps to manage deployment: [Microsoft 365 Copilot Chat for Students 13+ \| Microsoft Community Hub](https://techcommunity.microsoft.com/blog/EducationBlog/microsoft-365-copilot-chat-for-students-13/4412957).

If you're an admin authorized to modify the EDU classification for your tenant members, you can do so using a PowerShell script. In the Microsoft Download Center, get the [Copilot for Education Control](https://www.microsoft.com/download/details.aspx?id=108133).

[Section titled: Pinning settings for Copilot Chat](https://learn.microsoft.com/en-us/copilot/manage#pinning-settings-for--chat)

## Pinning settings for Copilot Chat

Copilot Chat is pinned by default for most users who are eligible for Copilot Chat. For tenants whose primary location is in the European Economic Area (EEA) or Switzerland, as of July 25, 2025, the _Pin Microsoft 365 Copilot Chat_ setting no longer governs the Microsoft 365 Copilot app. But this setting can still be used to control pinning within other Microsoft 365 apps. Chat will be visible in the navigation of the M365 Copilot app.

Get more details on [how to manage the pinning settings](https://learn.microsoft.com/en-us/copilot/microsoft-365/pin-copilot) of Copilot Chat in the navigation bar of Microsoft 365 apps for your users. You can also [pin the Microsoft 365 Copilot app to the Windows taskbar](https://learn.microsoft.com/en-us/copilot/microsoft-365/pin-copilot-taskbar).

The following video outlines the advantages of pinning the Microsoft 365 Copilot app to the Windows taskbar. It's 1 minute and 27 seconds long.

Embedded Video \| Microsoft Learn

0sfast\_forward

0sfast\_rewind

Skip Ad

play\_arrow0:00

volume\_up

fullscreenmore\_vert

_closed\_caption\_disabled_ CaptionsOff_settings_ ResolutionAuto_language_ Language_picture\_in\_picture\_alt_ Picture-in-PictureOff_cast_ Cast...Off_slow\_motion\_video_ Playback speed0x_control\_camera_ Recenter_3d\_rotation_ Toggle stereoscopic_cast_ Cast...

_arrow\_back_ CaptionsOff _done_

_arrow\_back_ ResolutionAuto _done_

_arrow\_back_ Language

_arrow\_back_ Playback speed0.5x0.75x1x1.25x1.5x1.75x2x

![Video preview image](https://videoencodingpublic-hgeaeyeba8gycee3.b01.azurefd.net/public-19ba8db4-4544-47aa-8454-c755fae69daa/Pin_Microsoft_365_Copilot_apps_to_the_taskbar_w1120.jpg)Play videoPlay Pin Microsoft 365 Copilot apps to the taskbar

If pinning is set to _Pin Copilot Chat in Microsoft 365 apps_, Copilot Chat is pinned in the Microsoft 365 Copilot app, Outlook, and Teams. It also becomes available in Word, Excel, PowerPoint, and OneNote via the Copilot button in the app ribbon.

Note

If pinning is set to _Do not pin Copilot Chat in Microsoft 365 apps_, Copilot Chat will not be available in Word, Excel, PowerPoint, or OneNote for users without a Microsoft 365 Copilot license, nor can users acquire it. Copilot Chat also will not be pinned in the Microsoft 365 Copilot app, Teams, and Outlook, but users can still acquire it through the App store unless admins restrict access in these surfaces specifically. Learn more about [removing access to Copilot Chat](https://learn.microsoft.com/en-us/copilot/manage#remove-access-to--chat).

In US government cloud environments, the pinning control only manages Copilot Chat availability in Word, Excel, PowerPoint, and OneNote. To manage availability in the Microsoft 365 Copilot app, Outlook, and Teams, please refer to [Remove access to Copilot Chat](https://learn.microsoft.com/en-us/copilot/manage#remove-access-to--chat).

[Section titled: Manage web search queries in Copilot Chat](https://learn.microsoft.com/en-us/copilot/manage#manage-web-search-queries-in--chat)

## Manage web search queries in Copilot Chat

To help improve the quality of responses, Copilot Chat can use web search queries sent to the Bing search service to ground responses in the latest information from the web. Learn more about [how generated web search queries work](https://learn.microsoft.com/en-us/copilot/privacy-and-protections#privacy-and-security-of-generated-search-queries) in Copilot Chat.

You can manage web search in Copilot Chat by using the **Allow web search in Copilot** policy, which is available in [Cloud Policy service for Microsoft 365](https://learn.microsoft.com/en-us/microsoft-365-apps/admin-center/overview-cloud-policy). The Allow web search in Copilot policy is also available in the settings section of the Copilot Control System page in the Microsoft 365 admin center. The policy allows web search to be managed at the tenant level and provides flexibility to modify for specific groups and users if the tenant has special requirements. The **Allow web search in Copilot** policy also allows you to manage web search for users with a Microsoft 365 Copilot license.

If you don't configure the **Allow web search in Copilot** policy, web search is available to users by default in both Microsoft 365 Copilot and Copilot Chat, unless you set the **Allow the use of additional optional connected experiences in Office** policy to Disabled. But turning off optional connected experiences restricts Microsoft 365 Copilot Chat, Microsoft 365 Copilot, and multiple experiences across Microsoft 365.

Note

For US Government Community Cloud (GCC) and Department of Defense (DoD) customers:

- Web search is available in GCC and DoD.
- The **Allow web search in Copilot** policy is available in GCC and DoD in Cloud Policy service for Microsoft 365.
- If the IT admin doesn't configure the **Allow web search in Copilot** policy, web search is turned off in GCC and DoD, regardless of how the **Allow the use of additional optional connected experiences in Office** policy is configured.

For more information on the **Allow web search in Copilot** policy, see [Data, privacy, and security for web queries in Microsoft 365 Copilot and Microsoft 365 Copilot Chat](https://learn.microsoft.com/en-us/copilot/microsoft-365/manage-public-web-access).

Note

If you turn off web search in Microsoft 365 Copilot Chat, web queries are not sent to the Bing search service and Copilot Chat uses only the underlying large language model (LLM) to generate responses.

[Section titled: Network requirements](https://learn.microsoft.com/en-us/copilot/manage#network-requirements)

## Network requirements

Microsoft 365 Copilot Chat adds generative AI capabilities to many Microsoft 365 applications by extending existing in-app features and introducing new ones. Admins can most effectively manage Microsoft 365 Copilot Chat experiences using in-service controls provided through the Microsoft 365 admin center (MAC) and individual applications.

Microsoft doesn't recommend and cannot support attempts to manage Microsoft 365 Copilot Chat and related settings through network-level restrictions such as selective domain, URL, IP blocking, or network-protocol filtering. Because Microsoft 365 Copilot Chat is deeply integrated with applications, such network-level restrictions can lead to unpredictable results and may cause failures or block access to those applications.

For the full list of Microsoft 365 required endpoints (which includes Microsoft 365 Copilot and Copilot Chat), please refer to [Microsoft 365 URLs and IP address ranges](https://learn.microsoft.com/en-us/microsoft-365/enterprise/urls-and-ip-address-ranges).

[Section titled: Copilot Chat usage report](https://learn.microsoft.com/en-us/copilot/manage#-chat-usage-report)

## Copilot Chat usage report

The Microsoft 365 Copilot Chat usage dashboard provides insights into active usage of Microsoft 365 Copilot Chat. Admins can generate reports on total active users, average daily active users, total prompts submitted and average prompts per user, and active users of Copilot Chat in specific apps. Learn how to get the Microsoft 365 Copilot Chat usage dashboard and how to use it in the documentation for [Microsoft 365 reports in the admin center](https://learn.microsoft.com/en-us/microsoft-365/admin/activity-reports/microsoft-copilot-usage).

[Section titled: How to ensure users access Copilot Chat](https://learn.microsoft.com/en-us/copilot/manage#how-to-ensure-users-access--chat)

## How to ensure users access Copilot Chat

Since January 2025, the Copilot experience _for work and education_ no longer shares the same name as the Copilot experience _for personal use_:

- **Microsoft 365 Copilot Chat** (grounded in the web) and **Microsoft 365 Copilot** (grounded in the web and work data) are for work and education. Entry points for users signed in with a Microsoft Entra account:

  - Microsoft 365 Copilot app (web, desktop, mobile)
  - copilot.cloud.microsoft
  - Copilot Chat in Edge
  - Copilot Chat in Word, Excel, PowerPoint, Outlook, OneNote, and Teams
- **Microsoft Copilot**is for personal use. Entry points for users signed in with a personal account (MSA):

  - Microsoft Copilot app (web, desktop, mobile)
  - copilot.microsoft.com
  - bing.com/chat
  - bing.com/copilotsearch
  - copilot.com
  - copilot.ai

To ensure your users access Copilot Chat (work and education), instruct them to access it from the Microsoft 365 Copilot app or on the web after signing in with their Entra account.

Additionally, you can manage whether your users can sign in to Microsoft 365 apps using a personal account (MSA). To manage user sign-in to Microsoft 365 apps using a personal account, [use tenant restrictions V2](https://learn.microsoft.com/en-us/entra/external-id/tenant-restrictions-v2).

[Section titled: Manage Copilot Chat in Edge](https://learn.microsoft.com/en-us/copilot/manage#manage--chat-in-edge)

## Manage Copilot Chat in Edge

Users can access Copilot Chat through the Copilot icon in the Edge browser UI when they're signed in with their Entra account.

Users can modify this permission by going to **Microsoft Edge > Settings > Appearance > Copilot and Sidebar > Copilot** and then turning on or off the toggles for _Show Copilot button on the toolbar_ and _Allow Microsoft to access page content_. An additional entry point to the Copilot in Edge policies is available in the settings section of the Copilot Control System page in the Microsoft 365 admin center, where group policies can be managed.

Admins can use multiple group policy settings to manage the behavior of the Copilot Chat in Edge sidebar:

- To allow or block Copilot Chat in Edge from using browsing context, use the [_EdgeEntraCopilotPageContext_](https://learn.microsoft.com/en-us/deployedge/microsoft-edge-policies#edgeentracopilotpagecontext) policy. This policy can prevent Copilot Chat from using webpage or PDF content when it formulates responses to prompts.
- To disable Copilot Chat in Edge entirely, use the [_HubsSidebarEnabled_](https://learn.microsoft.com/en-us/deployedge/microsoft-edge-policies#hubssidebarenabled) policy. Blocking Copilot Chat in Edge automatically blocks all Edge sidebar apps from being enabled.
- To allow or block Copilot Chat in Edge from using browsing context when users are signed in with their personal MSA Bing account while in the Edge work profile, use the [_CopilotPageContext_](https://learn.microsoft.com/en-us/deployedge/microsoft-edge-policies#copilotpagecontext) policy. This policy prevents Microsoft Copilot (personal use) from using webpage or PDF content when it formulates responses to prompts.

[Section titled: Mapping the Copilot key](https://learn.microsoft.com/en-us/copilot/manage#mapping-the--key)

## Mapping the Copilot key

The Copilot key was introduced to some PC keyboards in 2024. It was originally intended to invoke Copilot in Windows, but this use shifted as we evolved Microsoft Copilot experiences on Windows to better address your feedback and needs.

[![Screenshot that shows the Microsoft key in a keyboard.](https://learn.microsoft.com/en-us/copilot/media/copilot/copilot-key-800.png)](https://learn.microsoft.com/en-us/copilot/media/copilot/copilot-key-raw.png#lightbox)

As we previously shared, Copilot in Windows was removed, and the Microsoft Copilot app is now only available to personal users authenticating with a Microsoft account. The Microsoft Copilot app does not work for commercial users authenticating with a Microsoft Entra account. Users who wish to use Copilot for work or education can access Copilot Chat in the Microsoft 365 Copilot app. With this change, IT admins may need to take steps to ensure employees authenticating with a Microsoft Entra account can access Copilot Chat in the Microsoft 365 Copilot app via the Copilot key.

We recommend that managed commercial and educational organizations remap the Copilot key to invoke the Microsoft 365 Copilot app for simplified access to Copilot Chat experiences designed for work and education. Find detailed instructions on how to [remap the Copilot key here](https://learn.microsoft.com/en-us/windows/client-management/manage-windows-copilot#policies-to-manage-the-copilot-key).

[Section titled: Manage Copilot Chat on the web, in the Microsoft 365 Copilot app, and in Outlook](https://learn.microsoft.com/en-us/copilot/manage#manage--chat-on-the-web-in-the-microsoft-365--app-and-in-outlook)

## Manage Copilot Chat on the web, in the Microsoft 365 Copilot app, and in Outlook

The Copilot app is an integrated app that provides Copilot Chat in the Microsoft 365 Copilot app (web, desktop, mobile) and in Outlook (web, desktop, mobile). It also supports Copilot Chat on the web. Admins can deploy the Copilot app or manage its availability in the app store for users or user groups from Integrated Apps in the Microsoft 365 admin center (MAC).

Learn more about how Teams apps can be extended to Outlook and the Microsoft 365 app and managed from [Integrated Apps in the Microsoft 365 admin center](https://learn.microsoft.com/en-us/microsoft-365/admin/manage/teams-apps-work-on-outlook-and-m365).

To manage availability for the Copilot app, select Copilot from Integrated Apps in the Microsoft 365 admin center. Then, select _All users in the organization can install_ or select _Specific users/group in the organization can install_ and specify users or user groups who should have access.

Turning off the _Let users access Microsoft apps in your tenant_ setting in Integrated Apps will not turn off the Copilot app. You will need to manage the Copilot app directly using the steps above.

Note

Blocking the Copilot app through Integrated Apps is a tenant-wide control for all users, including those users assigned a Microsoft 365 Copilot license. Using this control blocks the Copilot app in the Microsoft 365 Copilot app and Outlook, and also blocks access to Copilot Chat on the web for all users. To remove access to the Copilot app only for users without a Microsoft 365 Copilot license while maintaining it for users with a Microsoft 365 Copilot license, please see [Removing access to Copilot Chat](https://learn.microsoft.com/en-us/copilot/manage#remove-access-to--chat).

[Section titled: Manage Copilot Chat in Teams](https://learn.microsoft.com/en-us/copilot/manage#manage--chat-in-teams)

## Manage Copilot Chat in Teams

Admins can manage Copilot Chat in Teams through the Copilot app in the [Teams admin center](https://learn.microsoft.com/en-us/microsoftteams/manage-apps). Like all other Teams apps, admins manage a single Copilot app in Teams for users with and without a license. To manage Microsoft 365 Copilot Chat, you should manage the users who don't have a Microsoft 365 Copilot license. For users who do have a Microsoft 365 Copilot license, you should confirm that they're assigned access to the app.

Admins can manage access and pinning for Microsoft 365 Copilot Chat. See [how to manage app access](https://learn.microsoft.com/en-us/microsoftteams/teams-app-permission-policies) and [how to pin Microsoft 365 Copilot Chat to the navigation bar](https://learn.microsoft.com/en-us/copilot/microsoft-365/pin-copilot).

[Section titled: Remove access to Copilot Chat](https://learn.microsoft.com/en-us/copilot/manage#remove-access-to--chat)

## Remove access to Copilot Chat

If you wish to prevent access to Microsoft 365 Copilot Chat for your users, follow these steps:

1. **Unpin Copilot Chat and block web access**: To change the pinning setting, use the control found under Settings on the Copilot Control System page in the Microsoft 365 admin center (MAC). Select _Do not pin Copilot Chat in Microsoft 365 apps_. This will unpin Copilot Chat in the Microsoft 365 Copilot app, Outlook, and Teams, and will make it unavailable in Word, Excel, PowerPoint, and OneNote. Learn more about [pinning Microsoft 365 Copilot Chat](https://learn.microsoft.com/en-us/copilot/microsoft-365/pin-copilot) for your entire tenant or for specific users or groups.

Copilot Chat users can still access it from m365.cloud.microsoft/chat even if _Do not pin Copilot Chat in Microsoft 365 apps_ is selected. You can manage access to the Copilot app through the Integrated Apps portal in the Microsoft 365 admin center (MAC) as described in Step 2.

2. **Microsoft 365 Copilot app and Outlook**: The Copilot app is an integrated app that provides Copilot Chat in the Microsoft 365 Copilot app (web, desktop, mobile) and Outlook (web, desktop, mobile). It also supports Copilot Chat on the web at m365.cloud.microsoft/chat. You can manage the Copilot app for these surfaces through the Integrated Apps portal in the Microsoft 365 admin center (MAC).

To prevent access to the Copilot app for unlicensed users, including US government customers, don't deploy the Copilot app to these users. To prevent the Copilot app from being available in the App store for unlicensed users, select _Specific users/group in the organization can install_. Then create a user group, or apply an existing group, with only Microsoft 365 Copilot licensed users. This will make the Copilot app unavailable for unlicensed users while keeping it available for licensed users. Learn more about these [Controls for managing Teams apps that work on Outlook and the Microsoft 365 Copilot app](https://learn.microsoft.com/en-us/microsoft-365/admin/manage/teams-apps-work-on-outlook-and-m365#controls-for-managing-teams-apps-that-work-on-outlook-and-the-microsoft-365-app).



Note



If you block the Copilot app using the Integrated app control, you will block the Copilot app tenant-wide across the Microsoft 365 Copilot app, Outlook, and the web, including for users assigned a Microsoft 365 Copilot license.

3. **Teams**: Only allow the Copilot app in Teams for users who are assigned a Microsoft 365 Copilot license—this will ensure your licensed users continue to have access to Copilot Chat. Don't allow it for users without a license. Learn more about [allowing users access to apps in Microsoft Teams](https://learn.microsoft.com/en-us/microsoftteams/teams-app-permission-policies). Don't pin the Copilot app in app setup policies for users without a Microsoft 365 Copilot license. You need to do this even if you selected _Do not pin Microsoft 365 Copilot Chat to the navigation bar_ in the Settings of the Copilot page in the Microsoft 365 admin center.

4. **Microsoft Edge**: Use the _EdgeMicrosoft365CopilotChatIconEnabled_ policy to control which sidebar apps, including Copilot Chat, are blocked (except the Search app).

You can find these URLs at edge://sidebar-internals. The sidebar internals JSON file includes a manifest for built-in sidebar apps, including a "target": {"url": "xyz"} parameter for each app. You can use these values to configure the policy.


[Section titled: Add recommended security protections for Copilot Chat](https://learn.microsoft.com/en-us/copilot/manage#add-recommended-security-protections-for--chat)

## Add recommended security protections for Copilot Chat

Microsoft helps you prepare for AI tools and companions while also building a strong foundation of security protection. Security recommendations for AI are based on Zero Trust, an industry-standard framework for security. By following these recommendations, you are building a Zero Trust foundation at the same time.

Introducing Copilot Chat to your environment provides the opportunity to tune-up security protections for web-grounded prompts. These include protections for user accounts, devices, and some app data. For more information, see [Apply principles of Zero Trust to Microsoft Copilot Chat](https://learn.microsoft.com/en-us/security/zero-trust/copilots/zero-trust-microsoft-copilot).

[![Screenshot that shows a staged approach to building security for AI tools and companions, starting with protections for web-grounded prompts with Copilot Chat.](https://learn.microsoft.com/en-us/copilot/media/copilot/copilot-chat-grounding-800.png)](https://learn.microsoft.com/en-us/copilot/media/copilot/copilot-chat-grounding-raw.png#lightbox)

Introducing Copilot to your environment allows you to take a staged approach, starting with protections for web-grounded prompts with Copilot Chat and maturing to protections for Microsoft 365 graph-grounded prompts. Protections for prompts grounded with data provided by your security tools (Security Copilot) focus on tuning up least privilege practices and honing threat protection. For more information, see [Use Zero Trust security to prepare for AI companions, including Microsoft Copilots](https://learn.microsoft.com/en-us/security/zero-trust/copilots/apply-zero-trust-copilots-overview).

* * *

## Additional resources

Training


Learning path


[Prepare your organization for Microsoft 365 Copilot - Training](https://learn.microsoft.com/en-us/training/paths/prepare-your-organization-microsoft-365-copilot/?source=recommendations)

This learning path examines the Microsoft 365 Copilot design and its security and compliance features, and it provides instruction on how to implement Microsoft 365 Copilot.


* * *

- Last updated on 03/03/2026

Ask Learn is an AI assistant that can answer questions, clarify concepts, and define terms using trusted Microsoft documentation.

Please sign in to use Ask Learn.

[Sign in](https://learn.microsoft.com/en-us/copilot/manage#)
