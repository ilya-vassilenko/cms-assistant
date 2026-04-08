<!-- Source: https://learn.microsoft.com/en-us/microsoft-365-apps/outlook/get-started/control-install -->

Table of contents Exit editor mode

Ask LearnAsk LearnFocus mode

Table of contents[Read in English](https://learn.microsoft.com/en-us/microsoft-365-apps/outlook/get-started/control-install)Add to CollectionsAdd to plan[Edit](https://github.com/MicrosoftDocs/outlook/blob/main/outlook/new-outlook-for-windows/get-started/control-install.md)

* * *

#### Share via

[Facebook](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fmicrosoft-365-apps%2Foutlook%2Fget-started%2Fcontrol-install%3FWT.mc_id%3Dfacebook) [x.com](https://twitter.com/intent/tweet?original_referer=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fmicrosoft-365-apps%2Foutlook%2Fget-started%2Fcontrol-install%3FWT.mc_id%3Dtwitter&tw_p=tweetbutton&url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fmicrosoft-365-apps%2Foutlook%2Fget-started%2Fcontrol-install%3FWT.mc_id%3Dtwitter) [LinkedIn](https://www.linkedin.com/feed/?shareActive=true&text=%0A%0D%0Ahttps%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fmicrosoft-365-apps%2Foutlook%2Fget-started%2Fcontrol-install%3FWT.mc_id%3Dlinkedin) [Email](mailto:?subject=%5BShared%20Article%5D%20Control%20Installing%20and%20Using%20New%20Outlook%20%7C%20Microsoft%20Learn&body=%0A%0D%0Ahttps%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fmicrosoft-365-apps%2Foutlook%2Fget-started%2Fcontrol-install%3FWT.mc_id%3Demail)

* * *

Copy MarkdownPrint

* * *

Note

Access to this page requires authorization. You can try [signing in](https://learn.microsoft.com/en-us/microsoft-365-apps/outlook/get-started/control-install#) or changing directories.


Access to this page requires authorization. You can try changing directories.


# Control installing and using new Outlook

Feedback

Summarize this article for me


This article provides guidance for administrators who want to control the installation of the new Outlook in an organization and how users access and use the app.

[Section titled: Prevent users from switching to new Outlook](https://learn.microsoft.com/en-us/microsoft-365-apps/outlook/get-started/control-install#prevent-users-from-switching-to-new-outlook)

## Prevent users from switching to new Outlook

Some administrators might choose to hide the **Try the new Outlook** toggle from appearing in the classic Outlook for Windows until the organization is ready to migrate the Outlook app.

Hiding the "new Outlook" toggle is available as a cloud policy in the Microsoft 365 Apps admin center. To set up the policy:

1. Sign in to the [Microsoft 365 Apps admin center](https://config.office.com/).
2. Under **Customization**, select **Policy Management**.
3. Select **Create**.
4. Search for the **Hide the "Try the new Outlook" toggle in Outlook** policy, and then enable it.

Alternatively, you can use the following Windows registry key to hide the **Try the new Outlook** toggle:

Console


Copy

```console
Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\Software\Microsoft\Office\16.0\Outlook\Options\General]
"HideNewOutlookToggle"=dword:00000000
```

To later enable the policy, set the registry key to 1:

Console


Copy

```console
Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\Software\Microsoft\Office\16.0\Outlook\Options\General]
"HideNewOutlookToggle"=dword:00000001
```

For more information about this process, see the [Use the registry to enable or disable the "Try the new Outlook" toggle in classic Outlook](https://learn.microsoft.com/en-us/exchange/clients-and-mobile-in-exchange-online/outlook-on-the-web/enable-disable-employee-access-new-outlook#use-the-registry-to-enable-or-disable-the-new-outlook-toggle-in-outlook-desktop) section of "Enable or disable user access to Outlook for Windows in Exchange Online."

[Section titled: Block new Outlook preinstallation on Windows](https://learn.microsoft.com/en-us/microsoft-365-apps/outlook/get-started/control-install#block-new-outlook-preinstallation-on-windows)

## Block new Outlook preinstallation on Windows

**Windows 11**

Windows 11 builds later than 23H2 have the new Outlook app preinstalled for all users. Currently, there isn't a way to block the new Outlook from being installed in these builds. If you prefer not to have new Outlook show up on your organization's devices, you can remove it after it's installed during the update.

To remove the app package, run the [Remove-AppxProvisionedPackage](https://learn.microsoft.com/en-us/powershell/module/dism/remove-appxprovisionedpackage) cmdlet by using the _PackageName_ parameter value, `Microsoft.OutlookForWindows`. After the package is removed, Windows updates won't reinstall new Outlook.

Run the following command in Windows PowerShell:

PowerShell


Copy

```powershell
Remove-AppxProvisionedPackage -AllUsers -Online -PackageName (Get-AppxPackage Microsoft.OutlookForWindows).PackageFullName
```

Additionally, remove the following Windows orchestrator registry value:

Console


Copy

```console
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\WindowsUpdate\Orchestrator\UScheduler_Oobe\OutlookUpdate
```

For any device that installed the March 2024 Non-Security Preview release (or later cumulative update) for Windows 11, version 23H2, Windows Orchestrator respects the deprovisioning cmdlet. Therefore, it's not necessary to remove this registry value in this case.

**Windows 10**

The new Outlook app is automatically installed on Windows 10 devices as part of the following updates:

- The optional Windows 10 release on January 28, 2025
- The monthly security update release for Windows 10 on February 11, 2025

To prevent the installation of new Outlook on your organization's devices, add the following registry value:

Console


Copy

```console
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\WindowsUpdate\Orchestrator\UScheduler_Oobe
```

Then, add a REG\_SZ registry setting that's named **BlockedOobeUpdaters**, and give it a value of `["MS_Outlook"]`.

To remove the app package after it's installed, run the [Remove-AppxProvisionedPackage](https://learn.microsoft.com/en-us/powershell/module/dism/remove-appxprovisionedpackage) cmdlet by using the _PackageName_ parameter value, `Microsoft.OutlookForWindows`.

Run the following command in Windows PowerShell:

PowerShell


Copy

```powershell
Remove-AppxProvisionedPackage -AllUsers -Online -PackageName (Get-AppxPackage Microsoft.OutlookForWindows).PackageFullName
```

After the package is removed, Windows updates won't reinstall new Outlook.

**User installations**

In cases of user installations (for example, if users use the toggle to install the new Outlook for Windows), run [Remove-AppxPackage](https://learn.microsoft.com/en-us/powershell/module/appx/remove-appxpackage). The AppxPackage cmdlets are used to manage applications for current users, and AppxProvisionedPackage cmdlets are used to manage default applications for both current and future users of the system.

Run the following Windows PowerShell command to remove the new Outlook for Windows for all users:

PowerShell


Copy

```powershell
Remove-AppxPackage -AllUsers -Package (Get-AppxPackage Microsoft.OutlookForWindows).PackageFullName
```

Tip

To verify that the app is installed, check whether the logs folder exists under: `%localappdata%\Microsoft\Olk\logs`. In some cases, users might not have the app installed but might see the pinned icon as a placeholder in the Start menu. The new Outlook app is then installed when users select the icon. You can manage Windows Start pins by following the instructions in [Customize the Start layout](https://learn.microsoft.com/en-us/windows/configuration/start/layout?tabs=intune-10%2Cintune-11&pivots=windows-11). Users might also see the new Outlook app in the **Recommended (Win11)** or **Suggested (Win10)** sections of the Start menu on consumer devices.

[Section titled: Block new Outlook installation as part of Mail and Calendar deprecation](https://learn.microsoft.com/en-us/microsoft-365-apps/outlook/get-started/control-install#block-new-outlook-installation-as-part-of-mail-and-calendar-deprecation)

## Block new Outlook installation as part of Mail and Calendar deprecation

Users can switch to new Outlook from the Mail and Calendar apps that are included in Windows. Support for Windows Mail and Calendar ended on December 31, 2024. We're automatically switching active users to the new Outlook app.

If you want to block users from getting the new Outlook from Windows Mail and Calendar applications, you can uninstall these apps from the user's devices.

To uninstall the apps, follow the instructions in [Remove-AppxProvisionedPackage](https://learn.microsoft.com/en-us/powershell/module/dism/remove-appxprovisionedpackage) to remove the app package by using the _PackageName_ parameter that has the value, `microsoft.windowscommunicationsapps`.

Run the following Windows PowerShell command:

PowerShell


Copy

```powershell
Get-AppxProvisionedPackage -Online | Where {$_.DisplayName -match "microsoft.windowscommunicationsapps"} | Remove-AppxProvisionedPackage -Online -PackageName {$_.PackageName}
```

To remove the Mail and Calendar apps for current users, run the following [Remove-AppxPackage](https://learn.microsoft.com/en-us/powershell/module/appx/remove-appxpackage) command in Windows PowerShell:

PowerShell


Copy

```powershell
Remove-AppxPackage -AllUsers -Package (Get-AppxPackage microsoft.windowscommunicationsapps).PackageFullName
```

Alternatively, you can remove the apps through Intune or by following the instructions in [Uninstall applications with Configuration Manager](https://learn.microsoft.com/en-us/mem/configmgr/apps/deploy-use/uninstall-applications).

[Section titled: Prevent users from acquiring new Outlook from Microsoft Store](https://learn.microsoft.com/en-us/microsoft-365-apps/outlook/get-started/control-install#prevent-users-from-acquiring-new-outlook-from-microsoft-store)

## Prevent users from acquiring new Outlook from Microsoft Store

The new Outlook for Windows app is also available in the Microsoft Store. To prevent users from downloading the app from the store, you can block store access by following the instructions in [Configure access to the Microsoft Store app](https://learn.microsoft.com/en-us/windows/configuration/store).

[Section titled: Opt out of new Outlook migration](https://learn.microsoft.com/en-us/microsoft-365-apps/outlook/get-started/control-install#opt-out-of-new-outlook-migration)

## Opt out of new Outlook migration

Admins can disable the user setting for automatic migration to prevent users from being switched to the new Outlook.

[Section titled: Policy: Manage user setting for new Outlook automatic migration](https://learn.microsoft.com/en-us/microsoft-365-apps/outlook/get-started/control-install#policy-manage-user-setting-for-new-outlook-automatic-migration)

#### Policy: Manage user setting for new Outlook automatic migration

The policy can be configured by using the following values:

- **Not set (Default)**: If you don’t configure this policy, the user setting for automatic migration remains uncontrolled, and users can manage it themselves. By default, this setting is enabled.
- **1 (Enable)**: If you enable this policy, the user setting for automatic migration is enforced. Automatic migration to the new Outlook is allowed, and users can't change the setting.
- **0 (Disable)**: If you disable this policy, the user setting for automatic migration is turned off. Automatic migration to the new Outlook is blocked, and users can't change the setting.

Note

This policy doesn't apply to migrations that are initiated through the "Admin-Controlled Migration to New Outlook" policy. For more information, see: [Admin-Controlled Migration Policy](https://learn.microsoft.com/en-us/microsoft-365-apps/outlook/manage/admin-controlled-migration-policy#hide-the-toggle-in-new-outlook-for-windows).

[Section titled: Configuring the policy using the Windows registry](https://learn.microsoft.com/en-us/microsoft-365-apps/outlook/get-started/control-install#configuring-the-policy-using-the-windows-registry)

#### Configuring the policy using the Windows registry

To disable automatic migration:

Console


Copy

```console
[HKEY_CURRENT_USER\Software\Policies\Microsoft\office\16.0\outlook\preferences]
"NewOutlookMigrationUserSetting"=dword:00000000
```

To enable automatic migration:

Console


Copy

```console
[HKEY_CURRENT_USER\Software\Policies\Microsoft\office\16.0\outlook\preferences]
"NewOutlookMigrationUserSetting"=dword:00000001
```

[Section titled: Setting in Group Policy](https://learn.microsoft.com/en-us/microsoft-365-apps/outlook/get-started/control-install#setting-in-group-policy)

#### Setting in Group Policy

You can download the latest Group Policy Administrative Template file from the [Microsoft Download Center](https://www.microsoft.com/download/details.aspx?id=49030).

[Section titled: Setting in Cloud Policy](https://learn.microsoft.com/en-us/microsoft-365-apps/outlook/get-started/control-install#setting-in-cloud-policy)

#### Setting in Cloud Policy

You can also set this policy through the [Cloud Policy](https://learn.microsoft.com/en-us/microsoft-365-apps/admin-center/overview-cloud-policy) service from the [Microsoft 365 Apps admin center](https://config.office.com/). For more information about Cloud Policy, see [Overview of Cloud Policy service for Microsoft 365](https://learn.microsoft.com/en-us/microsoft-365-apps/admin-center/overview-cloud-policy).

Tip

You can manage this setting in Intune using Administrative Template files because it's an ADMX policy. For more information, see [Use Windows 10/11 templates to configure group policy settings in Microsoft Intune](https://learn.microsoft.com/en-us/mem/intune/configuration/administrative-templates-windows?tabs=template). Download the latest ADMX template from [Microsoft Download Center](https://www.microsoft.com/en-us/download/details.aspx?id=49030&msockid=22d43a6aa2e46c5b0a7c29aea3576d18).

[Section titled: Conditional access to the new Outlook App](https://learn.microsoft.com/en-us/microsoft-365-apps/outlook/get-started/control-install#conditional-access-to-the-new-outlook-app)

## Conditional access to the new Outlook App

Many organizations have common access concerns that Conditional Access policies can help resolve. For example:

- Requiring multifactor authentication for users
- Blocking or granting access from specific locations
- Blocking risky sign-in behaviors
- Requiring organization-managed devices to be used

A more granular control can be offered by using OWA Mailbox Policies together with the _ConditionalAccessPolicy_ parameter. For example, when users are on noncompliant devices, OWA mailbox policies limit their capabilities. For example, restricting attachments.

To learn more about Conditional Access and how to configure it, follow the instructions in [Require compliant, hybrid joined devices, or MFA to grant or block access](https://learn.microsoft.com/en-us/entra/identity/conditional-access/howto-conditional-access-policy-compliant-device). To configure OWA Mailbox Policies, check [OWA Mailbox Policy - Conditional Access Policy](https://learn.microsoft.com/en-us/powershell/module/exchange/set-owamailboxpolicy).

[Section titled: Block mailbox access on new Outlook](https://learn.microsoft.com/en-us/microsoft-365-apps/outlook/get-started/control-install#block-mailbox-access-on-new-outlook)

## Block mailbox access on new Outlook

Users might acquire the new Outlook app through various flows, as outlined in the previous sections. To prevent mailbox access from the new Outlook, regardless of how users acquire it, use an Exchange mailbox policy to block organization (work or school) mailboxes from being added to the app. This policy serves as the final block, making sure that users can't use their work or school accounts even if they have the app on their device.

Mailbox policies are applied to the work or school email account and not at the device or app level. Therefore, to prevent users from using the app together with other accounts that aren't their work or school email account, we recommend that you block access to the app (as discussed in previous sections).

To manage mailbox access, follow the instructions in [Enable or disable user access to Outlook for Windows in Exchange Online](https://learn.microsoft.com/en-us/exchange/clients-and-mobile-in-exchange-online/outlook-on-the-web/enable-disable-employee-access-new-outlook#enable-or-disable-the-new-outlook-for-windows-for-an-individual-mailbox).

**Note:** The author created this article with assistance from AI. [Learn more](https://learn.microsoft.com/principles-for-ai-generated-content)

* * *

## Feedback

Was this page helpful?


YesNoNo

Need help with this topic?


Want to try using Ask Learn to clarify or guide you through this topic?


Ask LearnAsk Learn

Suggest a fix?

* * *

## Additional resources

Training


Module


[Use Microsoft 365 services with model-driven apps and Microsoft Dataverse - Training](https://learn.microsoft.com/en-us/training/modules/use-services-model-driven-apps/?source=recommendations)

Learn how to use Microsoft 365 services with Power Apps model-driven apps and Dynamics 365 customer engagement apps.


Certification


[Microsoft Office Specialist: Outlook Associate (Office 2019) - Certifications](https://learn.microsoft.com/en-us/credentials/certifications/mos-outlook-2019/?source=recommendations)

Demonstrate that you have the skills needed to get the most out of Outlook 2019 by earning the Microsoft Office Specialist (MOS) certification.


* * *

- Last updated on 03/09/2026

Ask Learn is an AI assistant that can answer questions, clarify concepts, and define terms using trusted Microsoft documentation.

Please sign in to use Ask Learn.

[Sign in](https://learn.microsoft.com/en-us/microsoft-365-apps/outlook/get-started/control-install#)
