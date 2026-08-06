import { Client } from '@microsoft/microsoft-graph-client';
import { TokenCredentialAuthenticationProvider } from '@microsoft/microsoft-graph-client/authProviders/azureTokenCredentials/index.js';
import { DefaultAzureCredential } from '@azure/identity';

export class GraphClient {
  private client: Client;
  private credential: DefaultAzureCredential;

  constructor(tenantId: string = 'common') {
    this.credential = new DefaultAzureCredential({
      tenantId,
    });

    const authProvider = new TokenCredentialAuthenticationProvider(this.credential, {
      scopes: ['https://graph.microsoft.com/.default'],
    });

    this.client = Client.initWithMiddleware({
      authProvider,
    });
  }

  getClient(): Client {
    return this.client;
  }

  async getMails(top: number = 10): Promise<any> {
    return this.client
      .api('/me/mailFolders/inbox/messages')
      .top(top)
      .select(['subject', 'from', 'receivedDateTime', 'hasAttachments'])
      .orderby('receivedDateTime DESC')
      .get();
  }

  async sendMail(to: string, subject: string, body: string): Promise<any> {
    const mailBody = {
      message: {
        subject,
        body: {
          contentType: 'HTML',
          content: body,
        },
        toRecipients: [
          {
            emailAddress: {
              address: to,
            },
          },
        ],
      },
    };

    return this.client.api('/me/sendMail').post(mailBody);
  }

  async getCalendarEvents(daysAhead: number = 7): Promise<any> {
    const startDate = new Date();
    const endDate = new Date(startDate.getTime() + daysAhead * 24 * 60 * 60 * 1000);

    return this.client
      .api('/me/calendarview')
      .query({
        startDateTime: startDate.toISOString(),
        endDateTime: endDate.toISOString(),
      })
      .select(['subject', 'start', 'end', 'organizer', 'attendees'])
      .orderby('start/dateTime')
      .get();
  }

  async createCalendarEvent(
    subject: string,
    startTime: Date,
    endTime: Date,
    attendees?: string[]
  ): Promise<any> {
    const event = {
      subject,
      start: {
        dateTime: startTime.toISOString(),
        timeZone: 'UTC',
      },
      end: {
        dateTime: endTime.toISOString(),
        timeZone: 'UTC',
      },
      attendees: attendees
        ? attendees.map((email) => ({
            emailAddress: {
              address: email,
            },
            type: 'required',
          }))
        : [],
    };

    return this.client.api('/me/events').post(event);
  }

  async getSharePointSites(): Promise<any> {
    return this.client.api('/me/sites').get();
  }

  async getSharePointFiles(siteId: string, driveId: string): Promise<any> {
    return this.client
      .api(`/sites/${siteId}/drives/${driveId}/root/children`)
      .select(['id', 'name', 'size', 'modifiedDateTime', 'webUrl'])
      .get();
  }

  async uploadFile(driveId: string, fileName: string, fileContent: Buffer): Promise<any> {
    return this.client
      .api(`/me/drive/root:/${fileName}:/content`)
      .put(fileContent);
  }

  async getUser(): Promise<any> {
    return this.client.api('/me').select(['displayName', 'mail', 'jobTitle']).get();
  }

  async searchUsers(query: string): Promise<any> {
    return this.client
      .api('/users')
      .filter(`startswith(displayName,'${query}') or startswith(mail,'${query}')`)
      .select(['displayName', 'mail', 'jobTitle'])
      .get();
  }
}
